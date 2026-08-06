from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from pathlib import Path
import os
import shutil
import re
import io
from ruamel.yaml import YAML
from .. import config

bp = Blueprint('tasks_admin', __name__, url_prefix='/admin/tasks')

yaml = YAML()
yaml.default_flow_style = False


def slugify(value: str) -> str:
    v = value or ''
    v = v.lower()
    v = re.sub(r"[^a-z0-9]+", "-", v)
    v = v.strip('-')
    if not v:
        v = 'task'
    return v


def tasks_dir() -> Path:
    # Use BASE_DIR from config when available, otherwise infer from app root
    base_dir = getattr(config, 'BASE_DIR', None)
    if base_dir:
        return Path(base_dir) / 'tasks'
    base = Path(current_app.root_path).parent
    return base / 'tasks'


def list_task_files():
    d = tasks_dir()
    if not d.exists():
        return []
    return sorted([p for p in d.iterdir() if p.suffix in ('.yml', '.yaml')])


def load_task(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return yaml.load(f)


def load_task_text(path: Path):
    # Return YAML text for editing
    with path.open('r', encoding='utf-8') as f:
        return f.read()


def backup_file(path: Path):
    bak = path.with_suffix(path.suffix + '.bak')
    shutil.copy2(path, bak)


def atomic_write(path: Path, data):
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        yaml.dump(data, f)
    tmp.replace(path)


def validate_task_data(data: dict):
    # Minimal validation to match ch_util.load_task expectations
    required = ['title', 'emoji', 'description']
    missing = [k for k in required if k not in data or not data[k]]
    return missing


@bp.route('/')
def index():
    files = list_task_files()
    tasks = []
    for p in files:
        try:
            data = load_task(p)
            title = data.get('title') if isinstance(data, dict) else None
        except Exception:
            title = None
        tasks.append({'file': p.name, 'title': title})
    return render_template('tasks_list.html', tasks=tasks)


@bp.route('/new', methods=('GET', 'POST'))
def new_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        slug = request.form.get('slug', '').strip() or slugify(title)
        raw_yaml = request.form.get('raw_yaml', '').strip()

        # Normalize name (no extension)
        name = os.path.splitext(slug)[0]
        if not name[0].isdigit():
            name = '1_' + name
        filename = name + '.yaml'
        path = tasks_dir() / filename

        try:
            if raw_yaml:
                data = yaml.load(raw_yaml)
            else:
                # Minimal structure
                data = {
                    'title': title or name,
                    'emoji': request.form.get('emoji', '📍'),
                    'description': request.form.get('description', ''),
                }
            missing = validate_task_data(data)
            if missing:
                flash(f"Missing required fields: {', '.join(missing)}", 'error')
                return render_template('task_form.html', task=data, is_new=True, raw_yaml_text=raw_yaml)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                flash('File already exists', 'error')
                return render_template('task_form.html', task=data, is_new=True, raw_yaml_text=raw_yaml)
            atomic_write(path, data)
            flash('Task created', 'success')
            return redirect(url_for('.index'))
        except Exception as e:
            flash(f'Error saving task: {e}', 'error')
            return render_template('task_form.html', task=request.form, is_new=True, raw_yaml_text=raw_yaml)

    # GET
    sample = {'title': '', 'emoji': '', 'description': ''}
    return render_template('task_form.html', task=sample, is_new=True, raw_yaml_text='')


@bp.route('/edit/<filename>', methods=('GET', 'POST'))
def edit_task(filename):
    # sanitize
    filename = os.path.basename(filename)
    path = tasks_dir() / filename
    if not path.exists():
        abort(404)

    if request.method == 'POST':
        raw_yaml = request.form.get('raw_yaml', '').strip()
        try:
            data = yaml.load(raw_yaml)
            missing = validate_task_data(data)
            if missing:
                flash(f"Missing required fields: {', '.join(missing)}", 'error')
                return render_template('task_form.html', task=data, filename=filename, is_new=False, raw_yaml_text=raw_yaml)
            backup_file(path)
            atomic_write(path, data)
            flash('Task updated', 'success')
            return redirect(url_for('.index'))
        except Exception as e:
            flash(f'Error saving task: {e}', 'error')
            return render_template('task_form.html', task=request.form, filename=filename, is_new=False, raw_yaml_text=raw_yaml)

    # GET
    data = load_task(path)
    raw_text = load_task_text(path)
    return render_template('task_form.html', task=data, filename=filename, is_new=False, raw_yaml_text=raw_text)


@bp.route('/delete/<filename>', methods=('POST',))
def delete_task(filename):
    filename = os.path.basename(filename)
    path = tasks_dir() / filename
    if not path.exists():
        abort(404)
    backup_file(path)
    path.unlink()
    flash('Task deleted (backup saved)', 'success')
    return redirect(url_for('.index'))
