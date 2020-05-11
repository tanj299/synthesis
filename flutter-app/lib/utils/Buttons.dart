import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import 'TextStyles.dart';
import 'consts.dart';
import 'package:flutter/foundation.dart';

class WideButtonGreen extends StatelessWidget {
  final String text;
  bool isBold=false;
  final GestureTapCallback onPressed;
  WideButtonGreen(this.text, this.onPressed);
  WideButtonGreen.bold(this.text, this.onPressed,this.isBold);

  @override
  Widget build(BuildContext context) {
    return ButtonTheme(
      minWidth: 350.0,
      height: 50.0,
      child: RaisedButton(
          color: Colors.green[300],
          shape: new RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(25)),
          child: isBold? BoldText(text,22.5,kwhite):NormalText(text, kwhite, 22.5),
        onPressed: onPressed,
    ));
  }
}

class WideButtonYellow extends StatelessWidget {
  final String text;
  bool isBold=false;
  final GestureTapCallback onPressed;
  WideButtonYellow(this.text, this.onPressed);
  WideButtonYellow.bold(this.text, this.onPressed,this.isBold);

  @override
  Widget build(BuildContext context) {
    return ButtonTheme(
      minWidth: 350.0,
      height: 50.0,
      child: RaisedButton(
          color: Colors.orange[300],
          shape: new RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(25)),
          child: isBold? BoldText(text,22.5,kwhite):NormalText(text, kwhite, 22.5),
        onPressed: onPressed,
    ));
  }
}

class WideButtonBlue extends StatelessWidget {
  final String text;
  bool isBold=false;
  final GestureTapCallback onPressed;
  WideButtonBlue(this.text, this.onPressed);
  WideButtonBlue.bold(this.text, this.onPressed,this.isBold);

  @override
  Widget build(BuildContext context) {
    return ButtonTheme(
      minWidth: 350.0,
      height: 50.0,
      child: RaisedButton(
          color: Colors.blue[300],
          shape: new RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(25)),
          child: isBold? BoldText(text,22.5,kwhite):NormalText(text, kwhite, 22.5),
        onPressed: onPressed,
    ));
  }
}

class SmallButtonGrey extends StatelessWidget {
  final String text;
  bool isBold=false;
  final GestureTapCallback onPressed;
  SmallButtonGrey(this.text, this.onPressed);
  SmallButtonGrey.bold(this.text, this.onPressed,this.isBold);

  @override
  Widget build(BuildContext context) {
    return ButtonTheme(
      minWidth: 50.0,
      height: 50.0,
      child: RaisedButton(
          color: Colors.grey[300],
          shape: new RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(25)),
          child: isBold? BoldText(text,22.5,kblack):NormalText(text, kblack, 22.5),
        onPressed: onPressed,
    ));
  }
}

class SquaredIcon extends StatelessWidget {
  final IconData icon;
  final String text;

  SquaredIcon(this.icon, this.text);

  @override
  Widget build(BuildContext context) {
    return  GestureDetector(
      onTap: ()=>null,
      child: Container(
        width: 50,
        height: 40,
        // decoration: new BoxDecoration(
        //   boxShadow: [
        //     BoxShadow(
        //       color: Colors.grey.shade500,
        //       blurRadius: 5.0,
        //       spreadRadius: -2.0,
        //       offset: Offset(
        //         3.0,
        //         4.0,
        //       ),
        //     )
        //   ],
        // ),
        child: Container(
            width: 45,
            height: 45,
            decoration: BoxDecoration(
                color: Colors.grey.shade200,
                borderRadius: BorderRadius.circular(10.0)
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Icon(icon,size: 25,color: kgreyDark,),
                SizedBox(
                  height: 2,
                ),
                NormalText(text,kblack,8.0)
              ],
            )),
      ),
    );
  }
}
