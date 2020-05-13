import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:lets_head_out/Screens/DashBoard.dart';
import 'package:lets_head_out/Screens/RegistrationScreen.dart';
import 'package:lets_head_out/utils/Buttons.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';
import 'package:lets_head_out/utils/forms.dart';

import 'Home.dart';

class SignInPage extends StatefulWidget {
  @override
  _SignInPageState createState() => _SignInPageState();
}

class _SignInPageState extends State<SignInPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kwhite,
      appBar: AppBar(
        elevation: 0.0,
        centerTitle: true,
        title: NormalText("Login", kblack, 20.0),
        backgroundColor: kwhite,
        iconTheme: IconThemeData(
          color: Colors.black,
        ),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            children: <Widget>[
              Icon(
                FontAwesomeIcons.seedling,
                color: Colors.green,
                size: 35,
              ),
              SizedBox(height: 10),
              BoldText("Synthesis", 30.0, Colors.green),
              NormalText("The Automatic Garden", Colors.lightGreen, 18.0),
              SizedBox(
                height: 30,
              ),
              Container(width: 340.0, child: NormalForm(Icons.email, "janesmith.synthesis@gmail.com", "Email")),
              SizedBox(
                height: 25,
              ),
              Container(
                width: 340.0,
                child: PasswordForm(),
              ),
              SizedBox(
                height: 10,
              ),
              Align(
                  alignment: Alignment.topCenter,
                  child: Padding(
                    padding: EdgeInsets.only(right: 8.0),
                    child: BoldText.veryBold(
                        "Forgot your password?", 12.5, kdarkBlue, true),
                  )),
              SizedBox(
                height: 25,
              ),
              WideButtonGreen.bold("Sign in", () {
                Navigator.push(context, MaterialPageRoute(builder: (_) {
                  return Home();
                }));
              }, true),
              SizedBox(
                height: 20,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  NormalText("Don't have an account?", kdarkBlue, 12.5),
                  SizedBox(
                    width: 5,
                  ),
                  GestureDetector(
                    onTap: () {
                      Navigator.of(context, rootNavigator: true)
                          .push(CupertinoPageRoute<bool>(
                        fullscreenDialog: true,
                        builder: (context) => RegistrationScreen(),
                      ));
                    },
                    child: Padding(
                      padding: EdgeInsets.only(
                        right: 8.0,
                      ),
                      child:
                          BoldText.veryBold("Register here", 12.5, Colors.green, true),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
