'use strict'

const express= require('express')
const https=require('https')
const fs=require('fs')
const path=require('path')
const app=express();

app.use('/',(req,res,next)=>{
res.send('This is an SSL Server !')
})

const options = {
  key:fs.readFileSync(path.join(__dirname,'./cert/key.pem')),
  cert:fs.readFileSync(path.join(__dirname,'./cert/cert.pem'))
}

const sslServer=https.createServer(options,app);
sslServer.listen(3000, '0.0.0.0', function() {
  console.log('Listening to port:  ' + 3000);
});
