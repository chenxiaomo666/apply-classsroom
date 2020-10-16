from apply_classroom import app


def main():
    app.run(host='0.0.0.0', port='2333', debug=False, ssl_context=("../ssl_cert/4634537_dev.mylwx.cn.pem", "../ssl_cert/4634537_dev.mylwx.cn.key"))


if __name__ == "__main__":
    main()
