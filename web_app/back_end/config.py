import os

basedir = os.path.abspath(os.path.dirname(__file__))
OROGINS = "http://localhost:8080"
UPLOAD_FOLDER = './static/'
PRODUCTION = True


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# Расширение Flask-SQLAlchemy принимает местоположение базы данных приложения из переменной конфигурации
# SQLALCHEMY_DATABASE_URI. Как вы помните из главы 3, в целом рекомендуется установить конфигурацию из переменных
# среды и предоставить резервное значение, когда среда не определяет переменную. В этом случае я беру URL-адрес базы
# данных из переменной среды DATABASE_URL, и если это не определено, я настраиваю базу данных с именем app.db,
# расположенную в основном каталоге приложения, которая хранится в переменной basedir.
#
#
# Параметр конфигурации SQLALCHEMY_TRACK_MODIFICATIONS установлен в значение False, чтобы отключить функцию
# Flask-SQLAlchemy, которая мне не нужна, которая должна сигнализировать приложению каждый раз, когда в базе данных
# должно быть внесено изменение.
