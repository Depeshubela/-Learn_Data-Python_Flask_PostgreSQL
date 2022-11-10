from app_blog import *
from flask_script import Manager, Command, prompt_bool, Shell
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)


manager.add_command('db', MigrateCommand)
'''
@manager.shell
def _make_context():
    return dict(app=app, db=db)

#manager.add_command("shell", Shell(make_context=_make_context))
'''

if __name__ == "__main__":
    manager.run()