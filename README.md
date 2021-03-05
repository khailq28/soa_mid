- Use mysql to create a database
- Execute file ibangking.sql to create table for database
- Ues Visual Studio Code to open folder SOA_MID
- In init.py, change app.config['SQLALCHEMY_DATABASE_URI'] = mysql+pymysql://yourUsername:yourPasswd@host/yourDatabasename 
- In terminal run: 'venv/Scripts/activate' and 'flask run'
- accounts: 
    Username            Passord
    ------------------  -------------
    khailuong           12345678
    bahuy123            12345678
    hoangkhang          12345678
- URIs:
    Endpoint          Methods    Rule
    ----------------  ---------  ---------------------------------
    api.getOtp        POST       /api/get_otp
    api.getSemester   POST       /api/get_semester
    api.getTuition    POST       /api/get_tuition
    api.getUserData   GET        /api/get_user_data
    api.payment       POST       /api/payment
    api.saveSemester  POST       /api/save_semester
    api.static        GET        /api/static/<path:filename>
    bootstrap.static  GET        /bootstrap/static/<path:filename>
    home              GET        /home
    login             GET, POST  /login
    login             GET        /
    logout            GET        /logout
    static            GET        /static/<path:filename>