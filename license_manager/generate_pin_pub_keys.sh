echo ////////// Start generating private and public keys ////// $2

cd $1
openssl genrsa -out $2.key && openssl rsa -in $2.key -pubout > $2.key.pub
cat $2.key.pub

echo /////////// Start generating private and public keys ///////
