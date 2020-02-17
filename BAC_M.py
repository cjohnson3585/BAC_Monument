"""
Main app script that calls everything for BAC_MONUMENT
"""

from flask import Flask, render_template, request

application = Flask(__name__)


@application.route("/")
def welcome():
    return render_template("input.html")



@application.route("/receiver", methods=['POST', 'GET'])
def receiver():
    if request.method=='POST':
        default_name = '0'
        wt = float(request.form.get('wt', default_name))
        abv = float(request.form.get('abv', default_name))
        tot = float(request.form.get('tot', default_name))
        sz = float(request.form.get('sz', default_name))
        hs = float(request.form.get('hs', default_name))
        ck = float(request.form.get('ck', default_name))
        bwig = wt*453.592#convert pounds to grams
        vod = (tot*sz)*29.5735#convert ounces to ml
        ott = calc_bac(vod, abv, bwig, ck, hs)#returns 2
        return ('{},{},{}'.format(round(ott[0],3),round(ott[1],3), ott[2]))


def calc_bac(vod, acod, bwig, rr, eth):
    msg = 'BAC LEGALLY OVER THE LIMIT: DO NOT DRIVE!'
    acig = vod*(acod/100.0)*0.789
    bac = acig/(bwig*rr)*100.0
    bact = bac - (eth*0.015)
    if bact > 0.0 and bact < 0.08:
        msg = 'LEGALLY IMPAIRED: YOU CAN BE ARRESTED WHILE DRIVING!'
    if bact <= 0.0:
        bact = 0.00
        msg = 'BAC NEAR 0.0: YOU CAN DRIVE!'
    return bac, bact, msg


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
