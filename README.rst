Semcomp-next
============

O próximo site da Semcomp!

Testando o site
===============

Primeiro, entre na pasta do site. Em seguida, tem que criar um ``virtualenv``:

::

    virtualenv env

O ``virtualenv`` é só uma maneira decente de controlar todas as dependências do
projeto: elas são instaladas localmente e nenhum outro pacote que não os
instalados ficam disponíveis para o aplicativo.

Depois de instalado, é preciso "ativá-lo":

::

    source env/bin/activate

Em seguida, é necessário instalar as dependências do site, que são um monte de
pacotes Python. **Vai** acontecer de ter pacotes que não vão instalar de
primeira por conta de dependências do sistema que não estão instaladas. Algumas
dessas dependências são ``libpng`` e ``libjpeg``. Há outras, mas não lembro
agora, vou esperar alguém reclamar pra colocar tudo :P

Pra instalar:

::

    pip install -r requirements/dev.txt

Depois de todos os problemas resolvidos, é hora de criar a base de dados. Na
versão local, está sendo usado ``sqlite`` como BD. O arquivo
``database.sqlite3`` no projeto é a base de dados, e está devidamente marcado
no arquivo ``.hgignore`` pra não ser incluído no repositório.

::

    python manage.py syncdb

O comando vai perguntar se você quer criar um super-usuário. Aproveite a
chance, dá menos dor de cabeça.

Quando o ``syncdb`` terminar, tem que fazer as migrações da base de dados. Nos
*updates* futuros, não será necessário usar o ``syncdb``, apenas os comandos
abaixo. O ``syncdb`` é necessário apenas na primeira rodada.

::

    python manage.py migrate

Depois disso, é só rodar o site! Ele ainda não tem por padrão as páginas que
deveria ter, mas estou trabalhando nisso.

::

    python manage.py runserver

Pra acessar o site, abra seu navegador favorito e acesse
``http://localhost:8000``

Problemas no site
=================

Comunique-os diretamente ou abra um incidente aqui:

https://bitbucket.org/fcoelho/semcomp-next/issues/new
