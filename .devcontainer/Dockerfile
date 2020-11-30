FROM linuxbrew/linuxbrew

RUN sudo apt-get upgrade -y 
RUN sudo apt-get update -y
RUN sudo apt-get install jq -y

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

#brew install tools
RUN brew install yarn
RUN brew install aws-cdk
RUN brew install docker
RUN brew install vim
RUN brew install kubectl
RUN brew install helm
RUN brew install gh
RUN brew install awscli 
RUN brew install pipenv
RUN brew install pulumi 
RUN brew install terraform 
RUN brew install node 
RUN brew install cdk8s 

RUN brew install starship
RUN echo 'eval "$(starship init bash)"' > ~/.bashrc

RUN brew install rbenv
RUN echo 'export PATH="$HOME/.rbenv/bin:$PATH"/neval "$(rbenv init)"' > ~/.bashrc
RUN rbenv install 2.7.2
RUN rbenv global 2.7.2
RUN echo 2.7.2 > ~/.ruby-version
RUN gem install terraspace 
