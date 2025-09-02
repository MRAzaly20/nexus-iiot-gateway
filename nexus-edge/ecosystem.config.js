module.exports = {
  apps: [{
    name: 'nexus-edge',
    //script: 'node_modules/.bin/next/dist/bin/next', //use this if you are using nextjs in windows environment
    script: 'node_modules/next/dist/bin/next', //use this if you are using nextjs in linux environment
    args: 'dev -p 3000',
    instances: 1,
    watch: false,
    autorestart: true,
  }]
};
