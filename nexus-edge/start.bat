@echo off
:: Masuk ke folder project
cd /d "C:\nexus-project\nexus-edge"

"C:\Users\Administrator\AppData\Roaming\npm\pm2.cmd" start ecosystem.config.js --env production
