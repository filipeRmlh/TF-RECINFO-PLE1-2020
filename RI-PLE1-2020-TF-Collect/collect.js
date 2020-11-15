
const {stream} = require('./services/api-service.js');
const fs = require('fs');

function getStreamData(data, output) {
    output.write(new Buffer.from(data));
}

async function connectAndStream(path, options){

    const output = fs.createWriteStream(path, {flags:'a'});

    try {
        stream(options)
            .then(res => res.data.on('data', data => {
                getStreamData(data,output);
            })).catch(e=>console.log('error: '+e))

    } catch (e) {
        console.log('stream error:');
        console.log(e);
    }
}

async function main() {

    await connectAndStream('twitter.txt', {
        'expansions': "author_id,referenced_tweets.id,referenced_tweets.id.author_id",
        'user.fields': "id,name",
        'tweet.fields': "referenced_tweets,lang"
    });
}

main();