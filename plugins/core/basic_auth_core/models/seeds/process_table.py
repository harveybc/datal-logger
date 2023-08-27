from ..user import User
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.util import sanitize_str
import warnings

_logger = logging.getLogger(__name__)

Base = automap_base()


# seed init data for processes tables, the tablesmust be listed also in the seed_init_data
def seed(app, db, table_name):
    with warnings.catch_warnings():
        #warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        warnings.simplefilter("ignore")

        with app.app_context():
            # sanitize the input string and limit its length
            table_name = sanitize_str(table_name, 256)
            Base.prepare(db.engine, reflect=False)
            # table base class
            table_base = eval("Base.classes." + table_name)
            # perform query
            try:
                if table_name == "gym_fx_config":
                    tmp0 =  table_base(initial_capital=10000, active=True)
                    tmp1 =  table_base(initial_capital=1000, active=False)
                    db.session.add(tmp0)
                    db.session.add(tmp1)
                    db.session.commit()
                    _logger.info("gym_fx_data table seeded") 
                elif table_name == "gym_fx_data":
                    tmp0 =  table_base(score=10000, score_v=9001, config_id=1)
                    tmp1 =  table_base(score=1000, score_v=900, config_id=2)
                    tmp2 =  table_base(score=1200, score_v=9900, config_id=1)
                    db.session.add(tmp0)
                    db.session.add(tmp1)
                    db.session.add(tmp2)
                    db.session.commit()
                    _logger.info("gym_fx_data table seeded") 
                elif table_name == "gym_fx_validation_plot":
                    # TODO: add reward, num_closes
                    tmp0 =  table_base(balance=10000, equity=10000, order_status= 0, reward=0, num_closes=0, config_id=2, tick_timestamp=0)
                    tmp1 =  table_base(balance=10000, equity=13000, order_status= 1, reward=0, num_closes=0 ,config_id=2, tick_timestamp=1)
                    tmp2 =  table_base(balance=12000, equity=12000, order_status= 0, reward=2000, num_closes=1 ,config_id=2, tick_timestamp=2)
                    tmp3 =  table_base(balance=12000, equity=7000, order_status= -1, reward=0, num_closes=1 ,config_id=2, tick_timestamp=3)
                    tmp4 =  table_base(balance=8000, equity=6000, order_status= 0, reward=-2000, num_closes=2,config_id=2, tick_timestamp=4)
                    tmp5 =  table_base(balance=9000, equity=8000, order_status= -1, reward=0, num_closes=2 ,config_id=2, tick_timestamp=5)
                    tmp6 =  table_base(balance=9000, equity=9000, order_status= 0, reward=0, num_closes=3 ,config_id=2, tick_timestamp=6)
                    tmp7 =  table_base(balance=9000, equity=11000, order_status= 1, reward=0, num_closes=3 ,config_id=2, tick_timestamp=7)
                    tmp8 =  table_base(balance=13000, equity=13000, order_status= 0 , reward=4000, num_closes=4,config_id=2, tick_timestamp=8)
                    tmp9 =  table_base(balance=13000, equity=12000, order_status= 1, reward=0, num_closes=4 ,config_id=2, tick_timestamp=9)
                    tmp10 =  table_base(balance=11000, equity=11000, order_status= 0 , reward=-2000, num_closes=5,config_id=2, tick_timestamp=10)
                    tmp11 =  table_base(balance=11000, equity=13000, order_status= 1, reward=0, num_closes=5 ,config_id=2, tick_timestamp=11)
                    db.session.add(tmp0)
                    db.session.add(tmp1)
                    db.session.add(tmp2)
                    db.session.add(tmp3)
                    db.session.add(tmp4)
                    db.session.add(tmp5)
                    db.session.add(tmp6)
                    db.session.add(tmp7)
                    db.session.add(tmp8)
                    db.session.add(tmp9)
                    db.session.add(tmp10)
                    db.session.add(tmp11)
                    
                    db.session.commit()
                    _logger.info("gym_fx_validation_plot table seeded") 
            except SQLAlchemyError as e:
                error = str(e)
                print("Error : " , error)

            