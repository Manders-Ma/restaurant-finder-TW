from hunter.connectDB import Session, Restaurant, Location, ParkingLot, Parking


with Session() as s:
    # query = """
    #     Select *
    #     FROM public.parking
    #     WHERE  "fk_Name"='MUME';
    # """
    # ParkingLots = s.execute(query)

    # print(type(ParkingLots))
    # for p in ParkingLots:
    #     print(p.fk_Name)
    
    fk_PL_ids = s.query(Parking.fk_PL_id).filter(Parking.fk_Name == 'MUME')
    specPL_id = []
    for id in fk_PL_ids:
        specPL_id.append(id[0])
        
    specParking = s.query(ParkingLot).filter(ParkingLot.PL_id.in_(specPL_id)).all()
    print(len(specParking))
    