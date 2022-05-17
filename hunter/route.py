from flask import render_template
from hunter.form import SearchForm
from hunter.connectDB import Session, Location, Restaurant
from hunter.MapModule import getRegionTown, calc_distance
import re


def index():
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        region, town = getRegionTown(form.address.data)
        # print("region is {}, town is {}".format(region, town))

        s = Session()
        lid = s.query(Location).filter(Location.Region == region).filter(
            Location.Town == town).all()[0].location_id
        s.commit()
        s.close()

        tables = calc_distance(location_id=lid, time_threshold=form.time.data,
                               origin=form.address.data, mode=form.mode.data, mode_para=form.mode_para.data)
        if tables:
            return render_template('index.html', form=form, tables=tables, count=len(tables))
        else:
            return render_template('index.html', form=form, count=len(tables))
    return render_template('index.html', form=form)


def park():
    return render_template('park.html')
