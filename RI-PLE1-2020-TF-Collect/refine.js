const readline = require('readline');
const fs = require('fs');

function getStreamData(tweetsObj, output) {
    for(const key in tweetsObj) {
        const value = tweetsObj[key];
        output.write(JSON.stringify(value)+"\n");
    }
}

function AddRefs(value, tweetsObj, filteredTweets) {
    let refAdded = false;
    if (value.data && value.data.referenced_tweets) {
        let ref = value.data.referenced_tweets;

        for(let i = 0; i < ref.length; i++) {
            const refId = ref[i].id;
            if (tweetsObj[refId]) {
                filteredTweets[refId] = tweetsObj[refId];
                refAdded = true;
            }
        }

    }
    return refAdded;
}

async function onLinesDone(tweetsObj, filtered, remain) {

    const filteredTweets = {};
    const remainedTweets = {};
    for(const key in tweetsObj) {
        const value = tweetsObj[key];
        let refAdded = AddRefs(value, tweetsObj, filteredTweets);
        if (refAdded) {
            filteredTweets[key] = value;
        } else {
            remainedTweets[key] = value;
        }
    }

    getStreamData(filteredTweets, filtered);
    getStreamData(remainedTweets, remain);

}

async function main() {
    const input = fs.createReadStream('twitter.txt');
    const filtered = fs.createWriteStream('twitter_filtered.txt', {flags:'a'});
    const remain = fs.createWriteStream('twitter_remain.txt', {flags:'a'});
    let lineReader = readline.createInterface({input});
    let tweetsObj = {};

    lineReader.on('line', function (line) {
        let tweetString = line.toString().trim();
        if (tweetString !== "") {
            let tweet = JSON.parse(tweetString);
            tweetsObj[tweet.data.id] = tweet;
        }

    });

    lineReader.on('close', ()=>{
        onLinesDone(tweetsObj, filtered, remain);
    })
}

main();