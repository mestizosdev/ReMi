## Oracle Instant Client

### Instalación del conector de Oracle en Mac OSX
* Descargar Oracle Instant Client. https://www.oracle.com/database/technologies/instant-client/downloads.html

        instantclient-basic-macos.x64-11.2.0.4.0.zip 
        instantclient-sqlplus-macos.x64-11.2.0.4.0.zip 
        instantclient-sdk-macos.x64-11.2.0.4.0.zip


* Descomprimir y copiar en un directorio todos los archivos, por ejemplo: /Users/allku/opt/instantclient_11_2

        libocci.dylib.11.1
        libociei.dylib
        libocijdbc11.dylib
        libsqlplus.dylib
        libsqlplusic.dylib
        ojdbc5.jar
        ojdbc6.jar
        sdk
        sqlplus
        uidrvci
        xstreams.jar
        
* Crear enlaces simbólicos en el terminal:

        ln -s libclntsh.dylib.11.1 libclntsh.dylib
        ln -s libocci.dylib.11.1 libocci.dylib

* Añadir al archivo .bash_profile: 

        vim .bash_profile 

        #Oracle Instant Client
        export ORACLE_HOME=/Users/allku/opt/instantclient_11_2
        export DYLD_LIBRARY_PATH=$ORACLE_HOME
        export LD_LIBRARY_PATH=$ORACLE_HOME
        export NLS_LANG=AMERICAN_AMERICA.UTF8
        export PATH=$PATH:$ORACLE_HOME

* Ejecutar: 

        source .bash_profile 

* Añadir el nombre del host al archivo /etc/hosts: 

       sudo vim /etc/hosts

       127.0.0.1       localhost       maclibro        maclibro.local

* Probar la conexión: 

        sqlplus lucila/l@//192.168.1.18:1521/orcl

* Instalar cx_Oracle: 

        pip3 install cx_oracle

### Instalación del conector de Oracle en Windows

* Descargar Oracle Instant Client. https://www.oracle.com/database/technologies/instant-client/downloads.html
        
        instantclient-basic-windows.x64-11.2.0.4.0.zip
        instantclient-sqlplus-nt-11.2.0.4.0.zip
        instantclient-sqlplus-windows.x64-11.2.0.4.0.zip
        
* Descomprimir y copiar en un directorio todos los archivos, por ejemplo: C:\instantclient_11_2

        sdk
        vc8
        vc9
        adrci.exe
        adrci.sym
        genezi.exe
        genezi.sym
        glogin.sql
        oci.dll
        oci.sym
        ocijdbc11.dll
        ocijdbc11.sym
        ociw32.dll
        ociw32.sym
        ojdbc5.jar
        ojdbc6.jar
        orannzsbb11.dll
        orannzsbb11.sym
        oraocci11.dll
        oraocci11.sym
        oraociei11.dll
        oraociei11.sym
        orasql11.dll
        orasql11.sym
        Orasqlplusic11.dll
        sqlplus.exe
        sqlplus.sym
        uidrvci.exe
        uidrvci.sym
        xstreams.jar

* Añadir C:\instantclient_11_2 al PATH: 

        1. Ejecutar el comando sysdm.cpl.
        2. Opciones avanzadas.
        3. Variables de entorno.
        4. Variables del sistema.
        5. Elegir de la lista la variable Path.
        6. Editar.
        7. En Valor de la variable, copiar al principio "C:\instantclient_11_2;" con punto y coma al final.

* Probar la conexión: 

        sqlplus lucila/l@//192.168.1.18:1521/orcl

* Instalar cx_Oracle: 

        pip3 install cx_oracle

### Instalación del conector de Oracle en Ubuntu.

* Descargar Oracle Instant Client. https://www.oracle.com/database/technologies/instant-client/downloads.html

        instantclient-basic-linux.x64-11.2.0.4.0.zip
        instantclient-sdk-linux.x64-11.2.0.4.0.zip
        instantclient-sqlplus-linux.x64-11.2.0.4.0.zip
        
* Descomprimir y copiar en un directorio todos los archivos, por ejemplo: /app/instantclient_11_2

        adrci
        genezi
        glogin.sql
        libclntsh.so.11.1
        libnnz11.so
        libocci.so.11.1
        libociei.so
        libocijdbc11.so
        libsqlplusic.so
        libsqlplus.so
        ojdbc5.jar
        ojdbc6.jar
        sdk
        sqlplus
        uidrvci
        xstreams.jar

* Crear enlaces simbólicos en el terminal:
        
        ln -s libclntsh.so.11.1 libclntsh.so
        ln -s libocci.so.11.1 libocci.so
        
* Crear el archivo oracle.conf y añadir la ruta:

        sudo vim /etc/ld.so.conf.d/oracle.conf
        
        /app/instantclient_11_2
        
* Ejecutar el comando e instalar las dependencias

        sudo ldconfig
        sudo apt install libaio-dev libaio1
        
* Añadir al archivo .bashrc: 

        vim .bashrc

        #Oracle Instant Client
        export LD_LIBRARY_PATH=/app/instantclient_11_2:$LD_LIBRARY_PATH
        export PATH=/app/instantclient_11_2:$PATH

* Ejecutar: 

        source .bashrc 
        
* Probar la conexión: 

        sqlplus lucila/l@//192.168.1.18:1521/orcl
        
* Instalar cx_Oracle

       pip3 install cx_oracle        
        