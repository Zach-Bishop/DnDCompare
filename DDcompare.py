# -*- coding: utf-8 -*-
import pandas as pd

class Chararmorclasster():
    def __init__(self, proficiencymodifier, dexmodifier,strengthmodifier,armorclass):
        self.proficiencymodifier=proficiencymodifier
        self.dexmodifier=dexmodifier
        self.strengthmodifier=strengthmodifier
        self.armorclass=armorclass
        self.chararmorclassterdf=pd.DataFrame()
        self.enemyhitdf=pd.DataFrame()
        self.save=False
    def __repr__(self):
        return "proficiencymodifierficiency: {0}, Dex Modifier: {1}, Strength Modifier: {2}".format(self.proficiencymodifier,self.dexmodifier,self.strengthmodifier)
    def damagecalc(self,weapon,proficiencymodifierficient=True,inspired='none'):
        if proficiencymodifierficient != True:
            proficiencymodifier=0+weapon.armorclasscurarmorclassybonus
        else:
            proficiencymodifier=self.proficiencymodifier+weapon.armorclasscurarmorclassybonus
        while True:
            if weapon.ds.lower()=='d':
                mod=self.dexmodifier
                break
            elif weapon.ds.lower()=='s':
                mod=self.strengthmodifier
                break
            else:
                print("invalid selection")
                break
        damagedict=computedamage(die=weapon.die,magic=weapon.magic,proficiencymodifier=proficiencymodifier,mod=mod,multipliedbonus=weapon.multipliedbonus,bonus=weapon.bonus,inspired=inspired)
        damagedf=pd.DataFrame.from_dict(damagedict).transpose()
        damagedf['Weapon Name']=weapon.name
        damagedf['Inspiration']=inspired
        if self.save==True:
            self.chararmorclassterdf=self.chararmorclassterdf.append(damagedf)
        return damagedf
    def bestweapon(self,armorclass,status='normal',matrix=False):
        if status not in self.chararmorclassterdf.index:
            return 'Error'
        elif armorclass not in self.chararmorclassterdf.columns:
            return 'Error'
        else:
            best=self.chararmorclassterdf.loc[self.chararmorclassterdf[armorclass]==max(self.chararmorclassterdf.loc[[status],armorclass]),'Weapon Name']
            while True:
                try:
                    best=best[0]
                    break
                except:
                    armorclass=armorclass+1
                    best=self.chararmorclassterdf.loc[self.chararmorclassterdf[armorclass]==max(self.chararmorclassterdf.loc[[status],armorclass]),'Weapon Name']
            if matrix==True:
                return best
            else:
                return 'Your best weapon is {}'.format(best)
    def bestweaponmatrix(self):
        Matrix=pd.DataFrame()
        for i in self.chararmorclassterdf.index:
            for j in range(10,25):
               Matrix.loc[i,j]=self.bestweapon(j,i,matrix=True)
        return Matrix
    def rememberdata(self):
        self.save=True
    def savecsv(self,filename):
        savedf=self.chararmorclassterdf.set_index(['Weapon Name',pd.Index(['Normal','Advantage','Disadvantage','Assassinate']*int(len(self.chararmorclassterdf)/4))])
        if filename[-4:]!='.csv':
            filename=str(filename)+'.csv'
        savedf.to_csv(filename)
    def computeenemyhit(self):
        damagerange={}
        hr={}
        for proficiencymodifier in range(0,20):
            hitchance=hitrate(0,0,proficiencymodifier,self.armorclass)
            hr[proficiencymodifier]=round(hitchance,3)
            damagerange['normal']=hr
        hr={}
        for proficiencymodifier in range(0,20):
            hitchance=advantage(0,0,proficiencymodifier,self.armorclass)
            hr[proficiencymodifier]=round(hitchance,3)
            damagerange['advantage']=hr
        hr={}
        for proficiencymodifier in range(0,20):
            hitchance=disadvantage(0,0,proficiencymodifier,self.armorclass)
            hr[proficiencymodifier]=round(hitchance,3)
            damagerange['disadvantage']=hr
        enemyhitdf=pd.DataFrame.from_dict(damagerange).transpose()
        if self.save==True:
            self.enemyhitdf=self.enemyhitdf.append(enemyhitdf)
        return enemyhitdf
class Weapon():
    def __init__(self,name,die, magic,multipliedbonus,ds,bonus=0,armorclasscurarmorclassybonus=0):
        self.name=name
        self.die=die
        self.magic=magic
        self.multipliedbonus=multipliedbonus
        self.ds=ds
        self.bonus=bonus
        self.armorclasscurarmorclassybonus=armorclasscurarmorclassybonus
    def __repr__(self):
        return "die: {0}, magic: {1}, multipided damage bonus={2}, dex or str: {3}, bonus: {4}, armorclasscurarmorclassy bonus: {5}".format(self.die,self.magic,self.multipliedbonus,self.ds,self.bonus,self.armorclasscurarmorclassybonus)
def hitrate(magic,proficiencymodifier,mod,armorclass):
    rate=((20+magic+proficiencymodifier+mod+1-armorclass))/20
    if rate>.95:
        rate=.95
    elif rate<.05:
        rate=.05
    return rate
def advantage(magic,proficiencymodifier,mod,armorclass):
    hr=hitrate(magic,proficiencymodifier,mod,armorclass)
    hit=hr+hr-hr*hr
    return hit
def disadvantage(magic,proficiencymodifier,mod,armorclass):
    hr=hitrate(magic,proficiencymodifier,mod,armorclass)
    hit=hr*hr
    return hit
def computedamage(die,magic,proficiencymodifier,mod,multipliedbonus,bonus,inspired='none'):
    damagerange={}
    if inspired.lower()=='damage':
        bonus=bonus+inspiration
    elif inspired.lower()!='none':
        proficiencymodifier=proficiencymodifier+inspiration
    dr={}
    for i in range(10,26):
        hitchance=hitrate(magic,proficiencymodifier,mod,i)
        damage=(die/2)*1.05+magic*1.05+.5*1.05+mod+multipliedbonus*1.05+bonus
        dr[i]=round(damage*hitchance,2)
    damagerange['normal']=dr
    dr={}
    for i in range(10,26):
        hitchance=advantage(magic,proficiencymodifier,mod,i)
        damage=(die/2)*1.075+magic*1.095+.5*1.095+mod+multipliedbonus*1.095+bonus
        dr[i]=round(damage*hitchance,2)
    damagerange['advantage']=dr
    dr={}
    for i in range(10,26):
        hitchance=disadvantage(magic,proficiencymodifier,mod,i)
        damage=(die/2)*1.0025+magic*1.0025+.5*1.0025+mod+multipliedbonus*1.0025+bonus
        dr[i]=round(damage*hitchance,2)
    damagerange['disadvantage']=dr
    dr={}
    for i in range(10,26):
        hitchance=advantage(magic,proficiencymodifier,mod,i)
        damage=(die/2)*2+magic*2+.5*2+mod+multipliedbonus*2+bonus
        dr[i]=round(damage*hitchance,2)
    damagerange['assassinate']=dr
    return damagerange
inspiration=3.5