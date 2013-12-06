============
Semcomp-next
============

O próximo site da Semcomp! Aqui tem uma explicação geral de como trabalhar com
cada parte do site. Tem links aos montes, cliquem neles!

.. note::
   Essas instruções estão escritas tomando Linux como o sistema operacional.
   Caso vá trabalhar no Windows, dê um toque que a gente vê como fazer tudo no
   por lá :)

Testando o site
===============

Há duas perspectivas para se trabalhar com o site: pelo ponto de vista do
*front end* e do ponto de vista do *back end*. *Front end* se refere ao
desenvolvimento da interface do site, HTML, CSS e Javascript. *Back end* se
refere à maquinaria que faz o site funcionar, neste caso Python e Django.

Trabalhando com o *front end*
*****************************

.. figure:: http://foundation.zurb.com/assets/img/homepage/hero-image.svg
   :height: 200px
   :width: 200px
   :align: right

O desenvolvimento do *front end* está dividido em três partes: HTML, CSS e
Javascript.

O site adota, como *framework*, `Foundation 5`_ (se sair um Foundation novo até
a época da Semcomp, dá pra pensar em atualizar se não estiver em cima da hora).
Olhar sempre na `documentação do Foundation`_ para implementar o que for
necessário.

HTML
----

Os arquivos HTML estão disponíveis dentro das pastas ``templates`` dentro das
pastas ``website``, ``account`` e ``management``. Para escrever os *templates*,
ver a `documentação de templates do Django`_.

CSS
---

O CSS do site é escrito inicialmente usando Sass_, especificamente usando a
sintaxe SCSS_. Também é necessário usar Compass_. Para instalar tudo necessário
para realizar alterações no CSS, seguir os passos abaixo.

Compass depende de uma instalação de Ruby_, não sei qual versão é a mínima
necessária. Uso 2.0.0 porque é a disponível pelo gerenciador de pacotes do
Fedora. Instale também RubyGems_ e em seguida é hora de instalar as *gems*!

Entre na pasta ``website/static/`` e digite:

.. code:: bash

   gem install bundler
   bundle install

Depois que as dependências estiverem instaladas, já é possível fazer alterações
no arquivo SCSS, que está localizado em ``website/static/sass/app.scss``. Pra
transformar as alterações no SCSS em CSS, ainda na pasta ``website/static/``
digite:

.. code:: bash

   compass watch

Isso vai iniciar o Compass no modo *watch*, que faz com que o CSS seja
atualizado toda vez que o SCSS sofrer alguma alteração.

Javascript
----------

O código javascript do site está em ``website/static/bower_components/``. Ele é
gerado "automaticamente" pelo Bower_. Novos arquivos Javascript podem ser
simplesmente colocados na pasta ``website/static/js/``, mas caso uma versão
nova de jQuery ou alguma outra dependência, pode-se usar o seguinte comando
para atualizar as dependências:

.. code:: bash

   bower update

Novos arquivos, como dito no parágrafo acima, podem ser colocados na pasta
``website/static/js``, mas deve-se dar preferência a evitar uma grande
quantidade de arquivos ``.js`` diferentes, pois isso vai tornar o cache de
Javascript do site bastante ineficiente.


.. _Foundation 5: http://foundation.zurb.com/
.. _documentação do Foundation: http://foundation.zurb.com/docs/
.. _documentação de templates do Django: https://docs.djangoproject.com/en/1.6/topics/templates/
.. _Sass: http://sass-lang.com/
.. _SCSS: http://sass-lang.com/documentation/file.SASS_REFERENCE.html#syntax
.. _Compass: http://compass-style.org/
.. _Ruby: https://www.ruby-lang.org/
.. _RubyGems: http://rubygems.org/
.. _Bower: http://bower.io/

Trabalhando com o *back end*
****************************

O *back end* do site está implementado usando Django_. Para rodar o site, é
necessário instalar uma série de dependências, os itens abaixo mostram como
instalar todos os pacotes necessários. Por enquanto, o site funciona com Python
2.7, ainda não é possível utilizar Python 3 por que algumas dependências ainda
não são compatíveis com Python 3.

Virtualenv
----------

É comum instalar as dependências de um projeto em Python de forma isolada do
sistema externo, para que o projeto funcione com somente os pacotes
necessários, reduzindo a chance de erros inesperados por conta de algum pacote
que está instalado em um lugar mas não em outro. Essa isolação é feita por uma
ferramenta chamada Virtualenv_. Depois de instalado o ``virtualenv``, entre na
pasta do site e execute:

.. code:: bash

   virtualenv env

Isso irá criar uma pasta chamada ``env`` que é um ambiente sem nenhum pacote
Python além dos disponibilizados pela biblioteca padrão, é um ambiente bastante
limpo. Depois de instalado o ``virtualenv``, é necessário ativá-lo para que as
dependências do projeto sejam instaladas diretamente nele, e não no sistema.

Para ativar o ``virtualenv``, execute:

.. code:: bash

   source env/bin/activate

O *prompt* do seu *shell* deve mudar para algo como ``(env)[user@host] $``
indicando que o ``virtualenv`` está ativo.

Instalar dependências
---------------------

O site depende de uma série de pacotes Python, sendo que um deles, chamado
``Pillow``, que é usado para manipulação de imagens, depende de bibliotecas
instaladas no sistema para saber como manipular imagens ``png`` e ``jpeg``, por
exemplo. É necessário instalar os pacotes ``libjpeg-devel`` ou ``libjpeg-dev``
e ``libpng-devel`` ou ``libpng-dev``, dependendo da distribuição que você use.

Depois de instaladas essas duas bibliotecas, é hora de instalar as dependências
diretas do site. Com o ``virtualenv`` ativo, execute:

.. code:: bash

   pip install -r requirements/dev.txt

Uma série de pacotes vai ser baixada, compilada e instalada dentro do
``virtualenv``. Quando o processo terminar, é possível ver uma lista dos
pacotes instalados executando o comando ``pip freeze``.

Banco de dados
--------------

O site necessita de um banco de dados para funcionar adequadamente (na verdade,
pra funcionar de qualquer jeito). Por padrão, durante o desenvolvimento é usado
um banco SQLite_, para não ter que instalar ainda mais dependências. Se alguém
quiser muito, é possível usar PostgreSQL, MySQL ou até SQL Server durante o
desenvolvimento.

Para criar o banco de dados, execute:

.. code:: bash

   python manage.py syncdb --noinput

Vai aparecer um arquivo chamado ``database.sqlite3`` na raíz do repositório,
ele é sua base de dados. Para terminar o processo, execute:

.. code:: bash

   python manage.my migrate

Depois de um monte de mensagens, o site está pronto para funcionar, mas é
necessário preenchê-lo com alguns dados iniciais.

Primeiros dados
---------------

Esse comando só deve ser executado uma vez, logo depois de realizar o
``migrate``. Caso esse comando seja executado depois que o site já tenha alguns
dados, eles serão sumariamente apagados, sem escrúpulos nem aviso. O comando
para criar os dados iniciais é:

.. code:: bash

   DJANGO_SETTINGS_MODULE=semcomp.settings.dev python default-pages.py

Executando o site
-----------------

Agora já é possível executar e testar o site, uhu! No terminal, digite:

.. code:: bash

   python manage.py runserver

Depois de alguns segundos o servidor web vai ser iniciado, é só abrir o seu
navegador favorito (até o IE vale se for pra ajudar a testar ;D ) e digitar na
barra de endereços::

    http://localhost:8000/

.. _Django: https://www.djangoproject.com/
.. _Virtualenv: http://www.virtualenv.org/en/latest/virtualenv.html
.. _SQLite: http://www.sqlite.org/


Problemas no site
=================

Comunique-os diretamente ou abra um incidente aqui:

https://github.com/fcoelho/semcomp-next/issues/new
