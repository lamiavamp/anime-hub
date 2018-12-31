from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Anime, User

engine = create_engine('sqlite:///anime.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#users

user1 = User(name ='lamia', email='lamia@xyz.com')
session.add(user1)
session.commit()

user_id = session.query(User).filter_by(email='lamia@xyz.com').one().id

##################
category1 = Category(name="Mecha")
session.add(category1)
session.commit()

anime1_1 = Anime(title="Code Geass", description='''In the year 2010, the Holy Empire of Britannia is establishing itself as a dominant military nation, starting with the conquest of Japan. Renamed to Area 11 after its swift defeat, Japan has seen significant resistance against these tyrants in an attempt to regain independence.''', category=category1, user_id=user_id)
session.add(anime1_1)
session.commit()


##################
category2 = Category(name="Shounen")
session.add(category2)
session.commit()

anime1_2 = Anime(user_id=user_id, title="Shingeki no Kyojin", description='''Centuries ago, mankind was slaughtered to near extinction by monstrous humanoid creatures called titans, forcing humans to hide in fear behind enormous concentric walls. What makes these giants truly terrifying is that their taste for human flesh is not born out of hunger but what appears to be out of pleasure. To ensure their survival, the remnants of humanity began living within defensive barriers, resulting in one hundred years without a single titan encounter.''', category=category2)
session.add(anime1_2)
session.commit()


##################
category3 = Category(name="School")
session.add(category3)
session.commit()

anime1_3 = Anime(title="Kaichou wa Maid-sama!", description='''Being the first female student council president isn't easy, especially when your school just transitioned from an all boys high school to a co-ed one. Aptly nicknamed "Demon President" by the boys for her strict disciplinary style, Misaki Ayuzawa is not afraid to use her mastery of Aikido techniques to cast judgment onto the hordes of misbehaving boys and defend the girls at Seika High School.''', category=category3, user_id=user_id)
session.add(anime1_3)
session.commit()

##################
category4 = Category(name="Adventure")
session.add(category4)
session.commit()

anime1_4 = Anime(title="Fairy Tail", description='''In the mystical land of Fiore, magic exists as an essential part of everyday life. Countless magic guilds lie at the core of all magical activity, and serve as venues for like-minded mages to band together and take on job requests. Among them, Fairy Tail stands out from the rest as a place of strength, spirit, and family.''', category=category4, user_id=user_id)
session.add(anime1_4)
session.commit()

##################
category5 = Category(name="Seinen")
session.add(category5)
session.commit()

anime1_5 = Anime(title="Fullmetal Alchemist", description='''Edward Elric, a young, brilliant alchemist, has lost much in his twelve-year life: when he and his brother Alphonse try to resurrect their dead mother through the forbidden act of human transmutation, Edward loses his brother as well as two of his limbs. With his supreme alchemy skills, Edward binds Alphonse's soul to a large suit of armor.''', category=category5, user_id=user_id)
session.add(anime1_5)
session.commit()

anime2_5 = Anime(title="Mirai Nikki", description='''Lonely high school student, Yukiteru Amano, spends his days writing a diary on his cellphone, while conversing with his two seemingly imaginary friends Deus Ex Machina, who is the god of time and space, and Murmur, the god's servant. Revealing himself to be an actual entity, Deus grants Yukiteru a "Random Diary," which shows highly descriptive entries based on the future and forces him into a bloody battle royale with 11 other holders of similarly powerful future diaries.''', category=category5, user_id=user_id)
session.add(anime2_5)
session.commit()

anime3_5 = Anime(title="Violet Evergarden", description='''The Great War finally came to an end after four long years of conflict; fractured in two, the continent of Telesis slowly began to flourish once again. Caught up in the bloodshed was Violet Evergarden, a young girl raised for the sole purpose of decimating enemy lines. Hospitalized and maimed in a bloody skirmish during the War's final leg, she was left with only words from the person she held dearest, but with no understanding of their meaning.''', category=category5, user_id=user_id)
session.add(anime3_5)
session.commit()

##################
category6 = Category(name="Josei")
session.add(category6)
session.commit()

anime1_6 = Anime(title="Hachimitsu to Clover", description='''Yuuta, Takumi, and Shinobu share a six-tatami room apartment with no bath. The rent is low and it's perfect for poor college students such as themselves. Shinobu is a mysterious, quirky person, who does things on a whim. Takumi is passionate both in work and love, and Yuuta is a simple person with simple dreams and desires. That is, until he meets Hagumi, a petite girl with enormous amount of talent. Hagumi is fondly called Hagu by Shuuji, who serves as Hagu's guardian. Hagu meets Ayumi, nicknamed Ayu, and they become close friends almost instantly. Meanwhile, Ayu falls for one of the boys...''', category=category6, user_id=user_id)
session.add(anime1_6)
session.commit()

##################
category7 = Category(name="Kodomomuke")
session.add(category7)
session.commit()

anime1_7 = Anime(title="Sailor Moon", description='''Usagi Tsukino is an average student and crybaby klutz who constantly scores low on her tests. Unexpectedly, her humdrum life is turned upside down when she saves a cat with a crescent moon on its head from danger. The cat, named Luna, later reveals that their meeting was not an accident: Usagi is destined to become Sailor Moon, a planetary guardian with the power to protect the Earth. Given a special brooch that allows her to transform, she must use her new powers to save the city from evil energy-stealing monsters sent by the malevolent Queen Beryl of the Dark Kingdom.''', category=category7, user_id=user_id)
session.add(anime1_7)
session.commit()

print "categories and anime added!"