subroutine FDFFT_vec(vector,vout,NP)
implicit none
include 'fftw3.f'
  integer         :: NP,dirn
  !real*8          :: vector(NP), vout(NP)
  double complex  :: vector(NP), vout(NP)
  !dimension       :: vector, vout(NP)
  integer*8       :: plan

  dirn=FFTW_FORWARD
  
  call dfftw_plan_dft_1d(plan,NP,vector,vout,dirn,FFTW_ESTIMATE)
  call dfftw_execute_dft(plan, vector, vout)
  call dfftw_destroy_plan(plan)

end subroutine FDFFT_vec

subroutine get_xaxis(xaxis,newaxis,npts,gridspace)
implicit none
integer          :: npts,i
real*8           :: xaxis(npts),newaxis(npts)
real*8           :: pa1,pa2,pa3,x,boxs,gridspace

  newaxis=0.d0

  boxs=npts*gridspace

     do i=0,npts-1
       if(i.le.npts/2) then
         x=2.d0*3.14159265358979323846264338d0*i/boxs

       else
         x=2.d0*3.14159265358979323846264338d0*(i-npts)/boxs

       endif
       newaxis(i+1)=x
     end do  

end subroutine get_xaxis


subroutine ntokens(line,ntok)
character,intent(in):: line*(*)
integer i, n, toks,ntok

i = 1;
n = len_trim(line)
toks = 0
ntok = 0
do while(i <= n)
   do while(line(i:i) == ' ') 
     i = i + 1
     if (n < i) return
   enddo
   toks = toks + 1
   ntok = toks
   do
     i = i + 1
     if (n < i) return
     if (line(i:i) == ' ') exit
   enddo
enddo
end subroutine ntokens

PROGRAM ft_timesort
  implicit none
  
  real*8,parameter       :: pi=3.14159265358979323846264338d0
  complex*16,parameter   :: zi=(0.d0,1.d0)
  integer                :: loadfile=1,i,j,N_time_steps,max_n_ele,file_stat,var_col,time_col,n_col,col_detect
  real*8                 :: R1,time_step,getval_line(20),getval,time,laserwl,laserfreq,getreal,getimag,getval10(10),maxv,minv,wid_gau,t_mid
  real*8                 :: window_cut=0.05,dt,dt_chk,max_load_val
  real*8,allocatable     :: T(:),FTX(:)
  complex*16,allocatable ::  DM(:),FTDM(:),readDM(:)
  real*8,allocatable     :: readT(:)
  character(255)         :: filename,chbuffer,fnameout
  character(600)         :: file_line
  character(2)           :: ch2
  integer                :: iargc,num_args,filenumber,N_include,num_cols,scale_option,trim_option
logical                  :: divfreq=.FALSE.,tok_set=.FALSE.,ignore_check_spacing=.FALSE.

  real*8,parameter            :: c_speed_AU=137.035999139d0,bohr2nm=0.0529177d0
  
  max_n_ele=10000000
  num_args=iargc()
  num_cols=1
  maxv=-9.d100
  minv=9.d100
  trim_option=0
  max_load_val=9.d99
  if(num_args==4) then
     call getarg(1,filename)
     call getarg(2,chbuffer)
     read(chbuffer,*) time_col
     call getarg(3,chbuffer)
     read(chbuffer,*) var_col
     call getarg(4,chbuffer)
     read(chbuffer,*) scale_option
  else if(num_args==5) then
     call getarg(1,filename)
     call getarg(2,chbuffer)
     read(chbuffer,*) time_col
     call getarg(3,chbuffer)
     read(chbuffer,*) var_col
     call getarg(4,chbuffer)
     read(chbuffer,*) scale_option
     call getarg(5,chbuffer)
     read(chbuffer,*) trim_option
  else if(num_args==6) then
     call getarg(1,filename)
     call getarg(2,chbuffer)
     read(chbuffer,*) time_col
     call getarg(3,chbuffer)
     read(chbuffer,*) var_col
     call getarg(4,chbuffer)
     read(chbuffer,*) scale_option
     call getarg(5,chbuffer)
     read(chbuffer,*) trim_option
     call getarg(6,chbuffer)
     read(chbuffer,*) max_load_val
  else if(num_args==7) then
     call getarg(1,filename)
     call getarg(2,chbuffer)
     read(chbuffer,*) time_col
     call getarg(3,chbuffer)
     read(chbuffer,*) var_col
     call getarg(4,chbuffer)
     read(chbuffer,*) scale_option
     call getarg(5,chbuffer)
     read(chbuffer,*) trim_option
     call getarg(6,chbuffer)
     read(chbuffer,*) max_load_val
     call getarg(7,chbuffer)
     read(chbuffer,*) ignore_check_spacing
  else
     print *, "Input: <file> <time_column> <Variable_column> <scale_option> <trim_opt> <max_val>"
	 print *, " *file will have 1 comment line, then 2 columns"
	 print *, " *if the width_gau is negative, it will be chosen based"
     print *, "     the width of the time axis"
	 print *, " *Scale Option: =0, do not scale or convert"
	 print *, " *Scale Option: =1, convert time in AU to wavelength in nm"
	 print *, " *trim_opt: =0, apply window to both ends"
	 print *, " *trim_opt: =1, only apply window to 2nd half"
	 
	 stop
  end if

  open(loadfile,file=trim(adjustl(filename))) 
  allocate(readT(max_n_ele),readDM(max_n_ele))
  N_include=0
  do i=1,max_n_ele
      read(loadfile,'(a)',IOSTAT=file_stat) file_line
      j=index(file_line,'#')
	  if(j>0) CYCLE
	  call ntokens(file_line,n_col)
	  if(tok_set==.FALSE.) then
	    col_detect=n_col
	    write(6,*) "Detected ",n_col," columns in the file"
        !read(loadfile,*,IOSTAT=file_stat) readT(i),getreal !,getimag
		tok_set=.TRUE.
	  end if
	  if(n_col/=col_detect) then
	    write(*,*) 'Change in number of columns to ',n_col," from ",col_detect,''
		write(*,*) 'After ',N_include,' lines. Reading for file will now stop'
	    exit
	  end if
	  if(file_stat .NE. 0) then
	    write(*,*) 'Error or End of file reached after ',N_include,' lines'
	    exit
	  end if
	  read(file_line,*) getval_line(1:n_col)
	  !write(6,*) getval_line(1:n_col)
	  N_include=N_include+1
	  if(abs(getval_line(var_col))>max_load_val) then
	    write(*,*) "point=",N_include," time=",getval_line(time_col)
		write(*,*) "value=",getval_line(var_col)," Will be set to 0.d0"
		getval_line(var_col)=0.d0
	  end if
	  readT(N_include)=getval_line(time_col)
	  readDM(N_include)=getval_line(var_col)
	  getval=getval_line(var_col)
	  if(getval>maxv) maxv=getval
	  if(getval<minv) minv=getval
	
  end do
  write(*,*) ' First time=',readT(1)
  write(*,*) ' Last time=',readT(N_include)
  write(*,*) ' Min Value=',minv
  write(*,*) ' Max Value=',maxv
  close(loadfile)
  
  ! make array of proper size and check times
  allocate(T(N_include),DM(N_include),FTDM(N_include),FTX(N_include))
  dt=readT(2)-readT(1)
  write(*,*) "Detect DT=",dt
  if(dt<1.d-8) then
    write(*,*) "dt is too small or times out of order"
	stop
  end if
  do i=1,N_include
     T(i)=readT(i)
	 DM(i)=readDM(i)
	 if((i>1).AND.(ignore_check_spacing==.FALSE.)) then
	   dt_chk=T(i)-T(i-1)
	   if(abs(dt_chk-dt)>1.d-3) then
	     write(*,*) "error in times. DT not consistent or times not in order!"
		 write(*,*) "i=",i-1," T=",T(i-1)
		 write(*,*) "i=",i," T=",T(i)
		 write(*,*) "dt=",dt_chk
		 stop
	   end if 
	 end if
  end do
  
  ! WINDOW  is exp(-((x-x0)/w)**6)
  ! window starts at width that gives t=0 a scale of window_cut
  t_mid=(T(N_include)+T(1))/2.d0
  
  wid_gau=(T(1)-t_mid)/((-LOG(window_cut))**(0.1666))
    write(*,*) "Detect wid_gau: Box width=",T(N_include)-T(1)
	write(*,*) " Use wid_gau=",wid_gau


  ! prep for FFT
  call get_xaxis(T,FTX,N_include,abs(T(2)-T(1)))
	
  ! do FFT without window
  call FDFFT_vec(DM,FTDM,N_include)
  write(ch2,'(i2.2)') var_col
  write(fnameout,'(a,a,a,a)') trim(adjustl(filename)),"_C",ch2,"_FFT_NO_WINDOW"
  write(*,*) "**Write out FFT with no window to:"
  write(*,'(a)') trim(adjustl(fnameout))
  open(1234,FILE=trim(adjustl(fnameout)),action='write',status='replace')
  !open(1235,FILE='FFT_real_imag.dat',action='write',status='replace')
  do i=1,N_include
     ! NOTE OLD WAS getval=conjg(FTDM(i))*FTDM(i)
	 getval=abs(FTDM(i))
	 if(scale_option==0) R1=FTX(i)*2*pi ! BUG ?
	 if(scale_option==1) R1=2*pi*bohr2nm*c_speed_AU/FTX(i)
     write(1234,*) R1,getval
	 !write(1235,*) FTX(i),real(FTDM(i)),imag(FTDM(i))
  end do  
  close(1234)
	
  write(fnameout,'(a,a,a,a)') trim(adjustl(filename)),"_C",ch2,"_WINDOW"
  write(*,*) "**Write out column with window applied to:"
  write(*,'(a)') trim(adjustl(fnameout))
  open(1234,FILE=trim(adjustl(fnameout)),action='write',status='replace')
  do i=1,N_include
     if(trim_option==0) then
	   DM(i)=DM(i)*exp(-((T(i)-t_mid)/wid_gau)**6)
     else if(trim_option==1) then
	   if(T(i)>t_mid) then
	     DM(i)=DM(i)*exp(-((T(i)-t_mid)/wid_gau)**6)
	   else
	     DM(i)=DM(i)
	   end if
	 end if
	 write(1234,'(3ES20.10E3)') T(i),real(DM(i)),real(readDM(i))
  end do
  close(1234)
  

  call FDFFT_vec(DM,FTDM,N_include)
  write(fnameout,'(a,a,a,a)') trim(adjustl(filename)),"_C",ch2,"_FFT"
  write(*,*) "**Write out FFT with window to:"
  write(*,'(a)') trim(adjustl(fnameout))
  open(1234,FILE=trim(adjustl(fnameout)),action='write',status='replace')
  !open(1235,FILE='FFT_real_imag.dat',action='write',status='replace')
  do i=1,N_include
     ! NOTE OLD WAS getval=conjg(FTDM(i))*FTDM(i)
	 getval=abs(FTDM(i))
	 if(scale_option==0) R1=FTX(i)*2*pi
	 if(scale_option==1) R1=2*pi*bohr2nm*c_speed_AU/FTX(i)
     write(1234,*) R1,getval
	 !write(1235,*) FTX(i),real(FTDM(i)),imag(FTDM(i))
  end do  
  close(1234)

  deallocate(readDM,readT,T,DM,FTDM,FTX)

END PROGRAM ft_timesort
