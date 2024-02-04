module.exports = {
  '*.ts': ['npx tsc --noEmit'],
  '*.{js,jsx,ts,tsx}': ['npx eslint --fix --config front_config/.eslintrc.yml'],
  '*.{js,jsx,ts,tsx,css}': ['npx prettier --write --config front_config/.prettierrc.yml']
};
