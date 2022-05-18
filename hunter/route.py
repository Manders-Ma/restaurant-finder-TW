from flask import render_template
from hunter.form import SearchForm, ParkingForm
from hunter.connectDB import Session, Location, Restaurant, Parking, ParkingLot
from hunter.MapModule import getRegionTown, calc_distance
import re


def index():
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        region, town = getRegionTown(form.address.data)
        # print("region is {}, town is {}".format(region, town))

        with Session() as s:
            lid = s.query(Location).filter(Location.Region == region).filter(
                Location.Town == town).all()[0].location_id
            s.commit()

        tables = calc_distance(location_id=lid, time_threshold=form.time.data,
                               origin=form.address.data, mode=form.mode.data, mode_para=form.mode_para.data)
        if tables:
            return render_template('index.html', form=form, tables=tables, count=len(tables))
        else:
            return render_template('index.html', form=form, count=len(tables))
    return render_template('index.html', form=form)


def park():
    form = ParkingForm(csrf__enabled=False)
    if form.validate_on_submit():
        with Session() as s:
            fk_PL_ids = s.query(Parking.fk_PL_id).filter(Parking.fk_Name == form.Rname.data)
            specPL_id = []
            for id in fk_PL_ids:
                specPL_id.append(id[0])
                
            specParkings = s.query(ParkingLot).filter(ParkingLot.PL_id.in_(specPL_id)).all()
        return render_template('park.html', form = form, specParkings=specParkings, count = len(specParkings))
    return render_template('park.html', form = form)
            
            
    return render_template('park.html')
