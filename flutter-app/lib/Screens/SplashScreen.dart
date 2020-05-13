import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';
import 'package:lets_head_out/utils/Buttons.dart';

// import 'BoardingView/OnBoardingScreen.dart';
import 'SignInPage.dart';

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

// SplashScreen == loading screen before anything is shown
class _SplashScreenState extends State<SplashScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        // backgroundColor: Colors.green,
        body: Container(
          width: MediaQuery.of(context).size.width,
          decoration: BoxDecoration(
              image: DecorationImage(
                  image: AssetImage("assets/bgimg_splash.jpg"),
                  fit: BoxFit.cover)),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Icon(FontAwesomeIcons.seedling,color: kwhite,size: 70,),
              SizedBox(height: 50),
              BoldText("Synthesis",35.0,Colors.green.shade800),
              TypewriterAnimatedTextKit(
                text: ["The Automatic Garden"],
                textStyle: TextStyle(fontSize: 30.0,color: kwhite,fontFamily: "nunito"),
                speed: Duration(milliseconds: 150),
              ),
              SizedBox(height: 25),
              WideButtonGreen.bold("Sign in", () {
                Navigator.push(context, MaterialPageRoute(builder: (_) {
                  return SignInPage();
                }));
              }, true),
            ],
          ),
        )

    );
  }

  // @override
  // void initState() {
  //   super.initState();
  //   Future.delayed(Duration(seconds:4 ),(){
  //     Navigator.push(context, MaterialPageRoute(builder: (_) {
  //       return SignInPage();
  //     }));
  //   });
  // }
}
