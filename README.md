# Synthesis
### Synthesis - The Automatic Garden
### Authors: Leo Au-Yeung, Daniel Mallia, Jayson Tan

This repository contains the code developed by the above authors in the 
Spring 2020 CSCI Capstone course under Professor Maryash at Hunter College, for 
the purpose of running an automated garden with a web interface. The hardware
heart of the project is a Raspberry Pi Model 3 B+ gathering data on a physical
garden with numerous sensors including tracking temperature, moisture, etc. 

### Set-up using Expo (for Mac OS ONLY)

1. Install Node.js 
2. After installing node (version 10.0 >), use npm to install Expo CLI to build react-native apps for iOS 
	~~~~
	npm install -g expo-cli
	~~~~
3. Ensure that XCode CLI is installed, otherwise install via: 
	~~~~
	xcode-select --install
	~~~~

...Or just download XCode from the App Store

4.  Since we are using Expo, start the script by running:
	~~~~
	expo start --ios
	~~~~

**If there are problems, you might need to 'source ~/.bash_profile' and include 'export PATH=$PATH:~/.npm-global/bin' in your '.bash_profile' file**
