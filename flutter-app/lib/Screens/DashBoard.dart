import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:lets_head_out/utils/BestRatedImage.dart';
import 'package:lets_head_out/utils/Buttons.dart';
import 'package:lets_head_out/utils/CitiesImage.dart';
import 'package:lets_head_out/utils/RecommendationImage.dart';
import 'package:lets_head_out/utils/TextStyles.dart';
import 'package:lets_head_out/utils/consts.dart';
import 'package:lets_head_out/utils/imageContainer.dart';

import 'OverViewScreen.dart';

class Dashboard extends StatefulWidget {
  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(

      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            // ImageContainer(),

            Padding(
              padding: const EdgeInsets.only(left:16.0,right: 16.0,bottom: 16.0),

              child: Column(children: <Widget>[
                SizedBox(
                  height: 40,
                ),
                Padding(
                  padding: const EdgeInsets.only(bottom: 16.0),
                  child: Align(
                      alignment: Alignment.center,
                      child: BoldText("Synthesis", 20.0, kblack)),
                ),
                Container(
                  width: 330,
                  height: 800,
                  child: ListView(
                    scrollDirection: Axis.vertical,
                    children: <Widget>[
                      buildContainer('Peralta', 'Orchid', 'johnsmith@gmail.com', 'Wed, 01 Apr 2020 23:35:02 GMT'),
                      buildContainer('Marianne', 'Lily', 'janesmith@gmail.com', 'Wed, 01 Apr 2020 23:36:28 GMT'),
                      buildContainer('Bobby', 'Orchid', 'bobbylee@gmail.com', 'Sun, 05 Apr 2020 15:25:16 GMT'),
                    ],
                  ),
                ),

              ]),
            ),
          ],
        ),
      ),
    );
  }



  Widget buildContainer(name, species, email, date) {
    return GestureDetector(
      onTap: (){
        Navigator.push(context, MaterialPageRoute(builder: (_) {
          return OverViewPage();
        }));
      },
      child: Container(
        width: 320,
        height: 200,
        child: Container(
            width: 300,
            height: 150,
            decoration: BoxDecoration(
                color: Colors.grey.shade50,
                borderRadius: BorderRadius.circular(15.0)),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: <Widget>[
                Container(
                  width: 100,
                  height: 100,
                  child: ClipRRect(
                      borderRadius: new BorderRadius.only(
                          topLeft: Radius.circular(15),
                          bottomLeft: Radius.circular(15)),
                      child: Icon(
                          Icons.local_florist,
                          color: kgreyDark,
                          size: 60.0,
                        ),
                      ),
                ),
                SizedBox(
                  width: 10.0,
                ),
                Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    BoldText(name, 20.5, kblack),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: <Widget>[
                        Icon(
                          Icons.local_florist,
                          color: kgreyDark,
                          size: 15.0,
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        BoldText("Species: " + species, 15.0, Colors.green),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: <Widget>[
                        Icon(
                          Icons.email,
                          color: kgreyDark,
                          size: 15.0,
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        NormalText(email, kgreyDark, 11.0),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: <Widget>[
                        Icon(
                          Icons.perm_identity,
                          color: kgreyDark,
                          size: 15.0,
                        ),
                        SizedBox(
                          width: 10,
                        ),
                        NormalText(date, kgreyDark, 11.0),
                      ],
                    ),
                    SizedBox(
                      height: 30,
                    ),
                    SizedBox(height: 14),
                  ],
                )
              ],
            )),
      ),
    );
  }
}
