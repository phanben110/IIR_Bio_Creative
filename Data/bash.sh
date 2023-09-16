sudo apt install curl
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.nvm/nvm.sh
nvm install v14.14.0
sudo add-apt-repository ppa:neovim-ppa/unstable
sudo apt-get update
sudo apt-get install neovim
cd
cd ~/.config/
git clone https://github.com/phanben110/nvim.git

nvim -c "PlugInstall" -c "qa"
nvim -c "CocInstall coc-json coc-tsserver" -c "qa"
nvim -c "CocInstall coc-python" -c "qa"
nvim -c "CocInstall coc-clangd" -c "qa"

echo "alias vi='nvim'" >> ~/.bashrc
echo "alias nv='nvim'" >> ~/.bashrc
sleep 2
source ~/.bashrc


echo "+++++++++++Install Neovim Sucessful++++++++"
