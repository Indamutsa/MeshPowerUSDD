from app import create_app

ussd_app  = create_app()

if __name__ == '__main__':
    ussd_app.run(debug=True)