from django.shortcuts import render,redirect,HttpResponse
from .models import *
import sweetify
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import qrcode
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime,date
from datetime import timedelta
import string
import random
# Create your views here.
def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(10))
    return random_string

def home (request):

    return render (request,'virtual-reality.html')
    

def login(request):
    if request.method=='POST':
        uname=request.POST['username']
        password=request.POST['password']
        try:
            data=Admin.objects.get(username=uname)
            if data.password==password:
                request.session ['username'] = uname
                sweetify.success(request,title="success",text="logged in successfully ..",button="close",timer=3000 )
                return redirect("index")
            else:
                messages.error(request, "In correct password !!!")
                # sweetify.error(request,title='Failed',text="incorrect password",button='close')
                return render(request,'sign-in.html')
        except:
            messages.error(request, "User Name not found !!!")
            # sweetify.error(request,title='Failed',text="username not found",button='close')
            return redirect('login')

    
    return render(request,'sign-in.html')
                
def index(request):
    if 'username' in request.session:
        combo=Pack.objects.all()
        c=len(combo)
        user=Userdata.objects.all()
        u=len(user)
        au=User_pack.objects.all().filter(pack_status='INACTIVE')
        actu=len(au)
        acuser=User_pack.objects.all().filter(pack_status='ACTIVE')
        auser=len(acuser)
        channel=Combo.objects.all()
        channel_avl=len(channel)
        context={
            'session':request.session['username'],
            'c':c,
            'u':u,
            'actu':actu,
            'auser':auser,
            'channel_avl':channel_avl,
        }
        return render(request,'index.html',context)
     
def register(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            data=Userdata.objects.get(email=email)
            if data.password==password:
                request.session ['email'] = email
                # sweetify.success(request,title="success",text="logged in successfully welcome..",button="close",timer=3000 )
                return redirect('user_index')
                # return render(request,'home.html',{'session':request.session['email']})
            else:
                sweetify.error(request,title='Failed',text="incorrect password",button='close',timer=3000)
                return render (request,'sign-up.html')
        except:
            sweetify.error(request,title='Failed',text="username not found",button='close',timer=3000)
            return redirect('register')

    return render (request,'sign-up.html')
    
def user_index(request):
    if 'email' in request.session:
        email=Userdata.objects.get(email=request.session['email'])
        print(email)
        try:
        # if 1==1:
            data=User_pack.objects.get(email_id=email.id)
            x=data.packname
            y=data.pack_status
            startdate=data.datef
            enddate=data.enddat
            current_date = datetime.now()
            end_date1 = datetime.combine(enddate, datetime.min.time())
            r_d=(end_date1-current_date).days
            print("printing rd",r_d)
            print(type(r_d))
            print(end_date1)
            print(current_date)
            id=data.user_id
            dr=r_d
            if r_d <= 0:
                de=Pack.objects.all().get(packname=data.packname)
                if de.pack_type == 'user_choice':
                    de.delete()
                data.delete()
                x=None
                y=None
                startdate=None
                enddate=None
                id=None
                dr=None

        except:
            x=None
            y=None
            startdate=None
            enddate=None
            id=None
            dr=None
            
        context={
            'session':request.session['email'],
            'x':x,
            'y':y,
            'enddate':enddate,
            "startdate":startdate,
            'id':id,
            'user':email.uname,
            'mob':email.mobileno,
            'dr':dr,

        }
        return render(request,'home.html',context)
    else:
         return redirect('home')
    
def user_logout(request):
    del request.session['email']
    return redirect('home')

def logout(request):
    del request.session['username']
    return redirect('home')

def newuser(request):
    if request.method=='POST':
        username=request.POST['uname']
        email=request.POST['email']
        mob=request.POST['mobno']
        password=request.POST['password']
        repass=request.POST['rpassword']
        try:
            user=Userdata.objects.get(email=email)
            messages.info(request, " Username already Taken !!!")
            return render (request,'newuser.html')
        except:
            if password==repass:
                udata=Userdata()
                udata.uname=username
                udata.email=email
                udata.mobileno=mob
                udata.password=password
                udata.save() 
                sweetify.success(request,title='success',text="registered sucessfully",button='close',timer=3000)
                return redirect('register')
            else:
                messages.error(request, "Password Must be Same !!!")
                return render (request,'newuser.html')
    else:
        return render(request,'newuser.html')
    
    
def combolist(request):
    if 'username' in request.session:
        data=Pack.objects.all()
        context={
            'data':data
        }
        return render (request,'combolist.html',context)
    else:
        context={'error':"login to access !!!"}  
        return render (request,'sign-up.html',context)


    
def channellist(request):
    if 'username' in request.session:
        data=Combo.objects.all()
        context={
            'data':data
        }
        return render (request,'channellist.html',context)
    
def add_combo(request):
    if 'username' in request.session:
        if request.method=="POST":
            combo_name=request.POST.get('Combo_name')
            # price=request.POST.get('price')
            print(combo_name)
            try:
                viewpack=Pack.objects.get(packname=combo_name)
                messages.error(request, "Pack name already Registered try something else !! ")
                return redirect('add_combo')
               
            except:
                data=Pack(packname=combo_name,price=0,pack_type="pre_defined")
                data.save()
                return redirect('add_channels',id=combo_name)     
        return render(request,"add_combo.html")
    
def add_channels(request,id):
    if 'username' in request.session:
        print(id)
        if request.method=="POST":
            comboname=request.POST.get('combo_name')
            channel_name=request.POST.get('channel_name')
            channel_price=request.POST.get('channel_price')
            channel_des=request.POST.get('channel_des')
            channel_lang=request.POST.get('channel_lang')
            channel_type=request.POST.get('channel_type')
            print(channel_type,channel_price,channel_des,channel_lang,channel_name,comboname)
            pack_ob=Pack.objects.get(packname=comboname)
            data=Combo()
            data.packname=pack_ob
            data.channelname=channel_name
            data.channelamount=channel_price
            data.channeldes=channel_des
            data.channeltype=channel_type
            data.channellang=channel_lang
            data.channelty='pre_defined'
            d=int(pack_ob.price)
            f=int(channel_price)
            pack_ob.price=d+f
            pack_ob.save()
            data.save()
        
            id=id
            return redirect('add_channels',id=id) 
        a=Pack.objects.get(packname=id)
        tvs=Combo.objects.all().filter(packname_id=a.id)
        print(tvs)
        context={
            'combo_name':id,
            'tvs':tvs,
        }
        return render(request,"add _channels.html",context)
    return HttpResponse("please login to access...")

def channel_del(request,id):
    if 'username' in request.session:
        print(id)
        delete_data=Combo.objects.get(id=id)
        id=delete_data.packname
        delete_data.delete()
        a=Pack.objects.get(packname=id)
        data=Combo.objects.all().filter(packname_id=a.id)
        v=0
        for i in data:
            v+= i.channelamount
        a.price=v
        a.save()
        return redirect('add_channels',id=id) 
    
def user_packs(request):
    if 'email' in request.session:
        data=Pack.objects.all()
        context={
        'data': data
        }
        return render(request,'user_packs.html',context)

def user_view_pack(request,id):
    if 'email' in request.session:
        fk=Pack.objects.get(id=id)
        data=Combo.objects.all().filter(packname_id=fk.id)
        print(data)
        content={
            'data':data,
            'fk':fk,
        }
        return render(request,"pack_details.html",content)
        

def pack_booking(request,id):
    if 'email' in request.session:
        fk=Pack.objects.get(id=id)
        data=Userdata.objects.get(email=request.session['email'])
        channel=Combo.objects.all().filter(packname_id=fk.id)
        try:
            userpack=User_pack.objects.get(email_id=data.id)
            print(userpack)
            if userpack.user_id != None and userpack.pack_status=='ACTIVE':
                messages.error(request,'PACK IS ALREADY IN ACTIVE SO PLEASE TRY AFTER THE PACK END..')
                return redirect('user_packs')
            elif userpack.user_id != None and userpack.pack_status=='INACTIVE':
                messages.info(request,'YOU HAVE ALREADY BOOKED A PACK PLEASE WAIT UNTILL CONFIRMATION !!!')
                return redirect('user_packs')

        except:
            print("except block running")
            qr_amount=fk.price
            qr_text = f"upi://pay?pa=prasanthguru003@okicici&pn=Guruprasanth&am={qr_amount}&cu=INR"
            qr_image = qrcode.make(qr_text, box_size=10)
            qr_image_pil = qr_image.get_image()
            stream = BytesIO()
            qr_image_pil.save(stream, format='PNG')
            qr_image_data = stream.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
            context={
            'qr_image_base64' : qr_image_base64,
            'id':fk
            }
            return render(request,'qrcode.html',context)    
    
def payment_done(request,id):
    if 'email' in request.session:
        print("payment option start running")
        fk=Pack.objects.get(packname=id)
        data=Userdata.objects.get(email=request.session['email'])
        channel=Combo.objects.all().filter(packname_id=fk.id)
        try:
            userpack=User_pack.objects.get(email_id=data.id)
            if userpack.user_id != None and userpack.pack_status=='INACTIVE':
                userpack.pack_status='ACTIVE'
                userpack.save()

        except:
                    print("except block is running")
                    x=datetime.now()
                    xe=str(x)
                    date=xe[0:10]
                    final_date=x+timedelta(days=28)
                    final_date1=str(final_date)
                    final_date2=final_date1[0:10]
                    from_date = datetime.strptime(date, "%Y-%m-%d")
                    to_date = datetime.strptime(final_date2, "%Y-%m-%d")
                    pen_date=to_date-from_date
                    diff=pen_date.days
                    pack_status="INACTIVE"
                    userid=78945612
                    print("entering into saving the block")
                    save_combo=User_pack(
                    email=data,
                    packname=fk,
                    pack_status=pack_status,
                    datef=date,
                    user_id=userid,
                    enddat=final_date2,
                    days_remaining=diff,
                    )
                    print("data stored in variable")
                    save_combo.save()
                    print("data saved success fully")
                   
    
        print("combo saved success fully !!!")
        subject = 'Registration success full'
        message = f'Hi {data.uname}, thanks for choosing the pack \n The pack name is :{fk.packname},\n the pack price is : {fk.price} ,\n your pack request has been submitted ,once approved by the admin your are able to view channels and the websites also....'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('user_index')

def user_view(request):
    if 'username' in request.session:
        data=User_pack.objects.all()
        context={
            'data':data,
        }
        return render(request,'view_user.html',context)
    
def activate_user(request,id):
    if 'username' in request.session:
        # id=id-1
        data=Userdata.objects.get(email=id)
        data_a=User_pack.objects.get(email_id=data.id)
        if data_a.pack_status == 'INACTIVE':    
            data_a.pack_status='ACTIVE'
            subject = 'Pack Activated'
            message = f'Hi {data.uname}, Your pack is success fully activated no u can able to view channels..thanks for choosing us !!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [data.email, ]
            send_mail( subject, message, email_from, recipient_list )
        else:
            data_a.pack_status='INACTIVE'
        data_a.save()
        print(data_a.pack_status)
        return redirect("user_view")

def pack_channel(request,id):
    if 'email' in request.session:
        te=Userdata.objects.get(email=request.session['email'])
        try:
            te1=User_pack.objects.get(email_id=te.id)
            messages.error(request,'PACK IS ALREADY IN ACTIVE SO PLEASE TRY AFTER THE PACK END..')
            return redirect('user_packs')
        except:
            fk=Pack.objects.get(id=id)
            data=Combo.objects.all().filter(packname_id=fk.id)
            ch_list=Combo.objects.all()
            all_ch=[]
            p_ch=[]
            for i in data:
                p_ch.append(i.channelname)
            for i in ch_list:
                all_ch.append(i.channelname)
            print(all_ch)
            li=[]
            s=set(all_ch)
            all_ch=list(s)
            print("first",all_ch)
            for i in p_ch:
                if i in all_ch:
                    all_ch.remove(i)
            print("second",all_ch)
            d=[]
            for i in all_ch:
                e=Combo.objects.all().filter(channelname=i)
                d.append(e)
            print("d is printing",d)
            context={'pack_name':fk,
                     'ex_ch':d,
                     'exis_ch':data,
                     }
            return render(request,'pack_channel.html',context)
    
def ex_ch(request):
    if request.method=='POST':
        extra_channel=request.POST.getlist('selected_channels')
        excisting_pack=request.POST.get('epackname')
        e_pack_ch=Pack.objects.all().get(packname=excisting_pack)
        ex_ch=Combo.objects.all().filter(packname=e_pack_ch)
        l=[]
        for i in extra_channel:
            d=Combo.objects.all().filter(id=i)
            l.append(d)
        print(l)
        for i in ex_ch:
            d=Combo.objects.all().filter(channelname=i)
            l.append(d)
        print("the total channels in adding",l)
        data=Pack.objects.all()
        ex=[]
        for i in data:
            ex.append(i.packname)
        print(ex)
        pack_new_name=generate_random_string()
        if pack_new_name in ex:
            pack_new_name=generate_random_string()
        new_pack=Pack()
        new_pack.packname=pack_new_name
        new_pack.price=0
        new_pack.pack_type='user_choice'
        for i in l:
            user=Combo()
            user.packname=new_pack
            x=[j.channelname for j in i]
            user.channelname=str(x[0])
            x=[j.channeldes for j in i]
            user.channeldes=str(x[0])
            x=[j.channelamount for j in i]
            user.channelamount=int(x[0])
            new_pack.price+=user.channelamount
            new_pack.save()
            x=[j.channeltype for j in i]
            user.channeltype=str(x[0])
            x=[j.channellang for j in i]
            user.channellang=str(x[0])
            user.channelty='user_defined'
            user.save()
           
        id=new_pack.id
        print(id)
        return redirect('pack_booking',id)
        

        
        # return HttpResponse('success')

def channel_view_user(request,id):
    fk=Pack.objects.get(packname=id)
    data=Combo.objects.all().filter(packname_id=fk.id)
    context={'exis_ch':data,
             'fk':fk}
    return render(request,'channel_view_user.html',context)