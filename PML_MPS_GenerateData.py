#%%

from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from lmfit import minimize, Parameters, Parameter, report_fit
import pandas as pd


#### Parameter 설정
hr_to_min =1/60 # 시간 단위 변환 hr을 min으로 변경하였습니다.

#### Organ volume
Vpan = 2.826 * 10**-6 # Volume of pancreas
Vmuscle = 537.7 * 10**-6 # Volume of pancreas
Vliver = 88.2*10**-6 # Volume of pancreas

#### Volume of blood in organ
Vbloodinpan = 0.89 * 10**-6 # Volume of blood in pancreas
Vbloodinmuscle = 169.1 * 10**-6# Volume of blood in muscle
Vbloodinliver = 27.73*10**-6# Volume of blood in liver
Vtotalblood = 225.4 * 10**-6# Volume of total blood
Vblood = Vtotalblood-Vbloodinpan -Vbloodinmuscle -Vbloodinliver # Volume of blood


#### Flow rate
Qpan = 31.99 * 10**-6 *hr_to_min#Flow rate in pancreas
Qmuscle = 301.1 * 10**-6*hr_to_min #Flow rate in muscle
Qliver = 1.398*10**-3*hr_to_min # Flow rate in liver

##
OrganVolume = [Vpan, Vmuscle, Vliver]
BloodVolume = [Vbloodinpan, Vbloodinmuscle, Vbloodinliver, Vtotalblood, Vblood]
Flowrate = [Qpan, Qmuscle, Qliver]
parameters = OrganVolume + BloodVolume + Flowrate

####Liver(간)에서의 glucsoe합성과 insulin 제거 파라미터 값
Prglu = 10*hr_to_min #간에서의 glucose 생성 (gluconeogenesis)
CLins = 200*hr_to_min #간에서의 insulin 제거 (clearance)

####Pancreas(췌장)에서 Insulin 분비 관련 파라미터 값, R[mU/L/hr] K[mM]
Rins = 4.3 * 10**5*hr_to_min # Maximum rate of insulin secretion
Kins = 2.4 * 10 #Constant of insulin secretion


#### Muscle(근육)에서 Glucsoe uptake관련 파라미터 값, R[/hr] K[mU/L] c[/hr]
Rglu = 1.7*hr_to_min # Maximum rate of glucose uptake dependent of insulin
Kglu = 2.6 * 10**3  # Constant of glucose uptake dependent of insulin
Cglu = 1.9*hr_to_min # Glucose uptake independent of insulin

 
def Glucose_Insulin_ODE(t,y, parameters): #Glucose-Insulin ODE를 풀기위한 함수 정의
    [Gpan,Gmuscle,Gliver,Gblood,Ipan,Imuscle,Iliver,Iblood] = y
    
    Vpan, Vmuscle, Vliver, Vbloodinpan, Vbloodinmuscle, Vbloodinliver, Vtotalblood, Vblood, Qpan, Qmuscle, Qliver = parameters

    
    dGpandt = (Qpan*Gblood - Qpan*Gpan)/Vbloodinpan # Pancreas에서의 glucsoe 농도 [mM]
    dGmuscledt = (Qmuscle*Gblood - Qmuscle*Gmuscle)/Vbloodinmuscle - (Vmuscle/Vbloodinmuscle)*Cglu*Gmuscle
    -(Vmuscle/Vbloodinmuscle)*((Rglu*Imuscle)/(Kglu + Imuscle))*Gmuscle# Muscle에서의 glucsoe 농도 [mM]
    dGliverdt = (Qliver*Gblood - Qliver*Gliver)/Vbloodinliver + (Vliver/Vbloodinliver)*Prglu# Liver에서의 glucose 농도 [mM]
    dGblooddt = (Qmuscle*Gmuscle + Qpan*Gpan + Qliver*Gliver - (Qpan + Qmuscle + Qliver)*Gblood)/Vblood# Blood에서의 glucsoe 농도 [mM]
    dIpandt = (Qpan*Iblood - Qpan*Ipan)/Vbloodinpan + (Vpan/Vbloodinpan)*((Rins*Gpan) / (Kins + Gpan))# # Pancreas에서의 insulin 농도 [mU]
    dImuscledt = (Qmuscle*Iblood - Qmuscle*Imuscle) / Vbloodinmuscle # # Muscle에서의 insulin 농도 [mU]
    dIliverdt = (Qliver*Iblood - Qliver*Iliver)/ Vbloodinliver - (Vliver/Vbloodinliver*CLins)*Iliver # Liver에서의 insulin 농도 [mU]
    dIblooddt = (Qpan*Ipan + Qmuscle*Imuscle + Qliver*Iliver - (Qpan+Qmuscle + Qliver)*Iblood)/Vblood # # Blood 에서의 insulin 농도 [mU]
    
    
    return [dGpandt, dGmuscledt, dGliverdt, dGblooddt, dIpandt, dImuscledt, dIliverdt, dIblooddt]

# Pancreas, Muscle, Liver, Blood에서 Glucose와 Inuslin 농도의 초기값 설정 
y0 = [16.6,# Glucose in Pancreas
      16.6,# Glucose in Muscle
      16.6,# Glucose in Liver
      16.6,# Glucose in Blood
      0,# Insulin in Pancreas
      0, #Insulin in Muscle
      0,# Insulin  in Liver
      0] #Insulin in Blood 

solution = solve_ivp(Glucose_Insulin_ODE,(0,180),y0, t_eval = np.linspace(0,180,19), args = (parameters,)) #Solve ivp를 이용하여 ODE 풀기, 시간은 0~180분으로 정의,
Time = solution.t


solution_data = np.append([Time], solution.y, axis = 0)

data_df = pd.DataFrame(solution_data.T, columns = ['Time','Gpan','Gmuscle','Gliver','Gblood','Ipan','Imuscle','Iliver','Iblood'])
data_df.to_csv("data.txt")


