import os
import re
import pathlib
import dotenv
dotenv.load_dotenv()

from invoke import task
from wanderift.wait import wait_for_pg

root_dir = pathlib.Path(__file__).parent


@task
def up(c):
    c.run("docker-compose up -d")

@task
def stop(c):
    c.run("docker-compose down")


@task
def down(c):
    c.run("docker-compose down -v")


@task
def reset(c, restore=None):
    c.run("docker-compose down -v")
    c.run("docker-compose up -d postgres redis")
    wait_for_pg()
    if restore:
        import dotenv
        dotenv.load_dotenv()
        db_user = os.getenv("POSTGRES_USER")
        db_host = os.getenv("POSTGRES_HOST")
        db_port = os.getenv("POSTGRES_PORT")
        db_name = os.getenv("POSTGRES_DB")
        db_password = os.getenv("POSTGRES_PASSWORD")
        conn_str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        c.run(f"psql -f '{restore}' {conn_str}")
    else:
        c.run("python manage.py migrate")
        c.run("python manage.py create_example_data")
        c.run("docker-compose up -d worker")


@task
def production_run(c):
    c.run("gunicorn -c wanderift/gunicorn_config.py wanderift.wsgi", pty=True)


JS_TEMPLATE = """export const {camelcase_name} = Vue.component('{kebab_name}', {{
    template: '#vue-{kebab_name}-template',
    delimiters: ['[[', ']]'],
}});
"""
HTML_TEMPLATE = """<script type="text/x-template" id="vue-{kebab_name}-template">
</script>
"""
INCLUDE_HTML = """{{% include "{path}" %}}\n"""
INCLUDE_JS = """<script type="module" src="{{% static "{path}" %}}"></script>\n"""


@task
def mc(c, kebab_name):
    camelcase_name = "".join([o.capitalize() for o in kebab_name.split("-")])
    js_dir = root_dir / "apps/home/static/home/js/vue/components"
    html_dir = root_dir / "apps/home/templates/home/vue/"
    js_file_name = js_dir / f'{kebab_name}.js'
    html_file_name = html_dir / f'{kebab_name}.html'
    for fname in (js_file_name, html_file_name):
        if fname.exists():
            print("File {fname} already exists")
            exit(1)
    templates_dir = root_dir / "apps/home/templates/home/"
    js_components_template = templates_dir / 'vue-js-components.html'
    html_components_template = templates_dir / 'vue-templates.html'
    with open(js_file_name, 'w') as f:
        f.write(JS_TEMPLATE.format(camelcase_name=camelcase_name, kebab_name=kebab_name))
    with open(html_file_name, 'w') as f:
        f.write(HTML_TEMPLATE.format(kebab_name=kebab_name))
    with open(js_components_template, 'a+') as f:
        f.write(INCLUDE_JS.format(path=f'home/js/vue/components/{kebab_name}.js'))
    with open(html_components_template, 'a+') as f:
        f.write(INCLUDE_HTML.format(path=f'home/vue/{kebab_name}.html'))
    print('Created files:')
    print(html_file_name)
    print(js_file_name)


@task
def worker(c):
    c.run("celery worker -A wanderift -l warning", pty=True)


@task
def static(c):
    c.run('python manage.py collectstatic --noinput -v 3')


@task
def deals(c):
    c.run('python manage.py fill_deals')


@task
def build_frontend(c):
    import os
    curdir = os.getcwd()
    frontend_dir = root_dir / 'frontend'
    os.chdir(frontend_dir)
    c.run('npm install')
    c.run('npm run build')
    os.chdir(curdir)


@task
def beat(c):
    c.run('celery -A wanderift beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler')
