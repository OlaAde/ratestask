from sqlalchemy.sql import text


def get_port_codes_for_region(db, region):
    query = """
        SELECT code FROM ports WHERE parent_slug IN 
        (WITH RECURSIVE regions_included AS 
        (SELECT slug FROM regions WHERE slug = :slug UNION SELECT r.slug FROM regions r INNER JOIN regions_included ri 
        ON r.parent_slug = ri.slug)
                          SELECT * FROM regions_included);
    """

    cursor = db.session.execute(text(query), {"slug": region})

    return cursor.fetchall()


def get_port_codes_for_region_or_return_port(db, region_or_port):
    port_codes_for_region = get_port_codes_for_region(db, region_or_port)
    port_codes_for_region = tuple([row[0] for row in port_codes_for_region])
    return port_codes_for_region if len(port_codes_for_region) > 0 else tuple([region_or_port])


def get_average_prices_between_dates_and_ports(db, date_from, date_to, port_codes_for_origin,
                                               port_codes_for_destination):
    query = """
        SELECT day, CASE WHEN count(day) > 2 THEN ceil(sum(price)/count(day)) END as price FROM prices 
        WHERE orig_code in :port_codes_for_origin AND dest_code in :port_codes_for_destination AND day IN 
        (SELECT i::DATE FROM generate_series(:date_from, :date_to, '1 day'::INTERVAL) i) GROUP BY day 
        ORDER BY day;
    """
    cursor = db.session.execute(text(query), {"date_from": date_from,
                                              "date_to": date_to,
                                              "port_codes_for_origin": port_codes_for_origin,
                                              "port_codes_for_destination": port_codes_for_destination
                                              })
    return cursor.fetchall()
