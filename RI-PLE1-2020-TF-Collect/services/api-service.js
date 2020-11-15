require('dotenv').config();
const axios = require('axios');

const bearerToken = process.env.BEARER_TOKEN;
const server = 'https://api.twitter.com';

const httpClient = axios.create({
    baseURL: server,
    headers: {
        "AUTHORIZATION" : `Bearer ${bearerToken}`,
    },
});

function get (path, params, configs, version = '1.1') {
    return httpClient.get(`/${version}/${path}`,{ params, ...configs });
}

function post (path, data, configs, version = '1.1') {
    return httpClient.post(`/${version}/${path}`, data, configs);
}

function getUsers(ids, options) {
    return get(`users`, {ids:ids.join(','), ...options}, '2')
}

function getTweets(ids, options) {
    return get('tweets', {ids: ids.join(','), ...options},{},'2');
}

function stream(options) {
    return get('tweets/sample/stream',  options,{responseType: 'stream'},'2');
}

function filteredStreamRules(data) {
    return post('tweets/search/stream/rules',  data,null,'2');
}

function filteredStream(params) {
    return get('tweets/search/stream',params,{responseType: 'stream'},'2');
}

function searchTweets(query, options, version='1.1') {
    let url = `${version==='1.1' ? '' : 'tweets'}/search/${version==='1.1' ? 'tweets.json' : 'recent'}`;
    options = options || {};
    if(version==='1.1'){
        options['q'] = query;
    } else {
        options['query'] = query;
    }
    return get(url, options);
}

function getRetweets(id, options, version='1.1') {
    return get(`statuses/retweets/${id}.json`, options, version);
}

module.exports = {
    stream,
    getTweets,
    filteredStream,
    filteredStreamRules,
    getUsers,
    getRetweets,
    searchTweets,
}