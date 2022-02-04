echo "Debugmail started, messages shown below.."
echo " "
python3 -m smtpd -c DebuggingServer -n localhost:1025
