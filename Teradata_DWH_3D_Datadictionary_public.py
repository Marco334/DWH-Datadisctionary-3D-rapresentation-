import teradata
import teradatasql
import pandas as pd
import bpy
import math
#RUN BLENDER AS ADMINISTRATOR !!!!
#MODIFY TABLE DICTIONARY IN DB_LIST
#pip install teradatasql
 

def DB_CONNECTION_MNG_1():
   print ( '\n INIZIO CONNESSIONE \n' )
   host,username,password = 'xxx.xxx.xxx.xxx','xxxxx', 'xxxx'
   udaExec = teradata.UdaExec (appName="HelloWorld", version="1.0",logConsole=False) 
   session = udaExec.connect(method="odbc", system=host,username="dbc", password="dbc");
   print( ' \n CONNESSIONE EFFETTUATA \n' )
   return(udaExec.connect(method="odbc", system=host,username="dbc", password="dbc"))

def Collection_MNG_1():
#--------- COLLECTION MANAGEMENT
   collection_T = bpy.data.collections.new('TABLES')
   bpy.context.scene.collection.children.link(collection_T)
   collection_V = bpy.data.collections.new('VIEW')
   bpy.context.scene.collection.children.link(collection_V)
   collection_X = bpy.data.collections.new('TEXT')
   bpy.context.scene.collection.children.link(collection_X)
   collection_S = bpy.data.collections.new('STAT_ALLERT')
   bpy.context.scene.collection.children.link(collection_S)
   return(1)

def Color_MNG_1():
    #The four values are represented as: [Red, Green, Blue, Alpha]
    ORAN  = bpy.data.materials.new(name="Orange_T"  ) #TEBLE - set new material to variable
    ORAN.diffuse_color = (0.98,0.225,0.01,1)
    GLASS = bpy.data.materials.new(name="Glass_V" ) #VIEW - set new material to variable
    GLASS.diffuse_color = (0.1, 0.5, 0.7,0)
    ROSSO = bpy.data.materials.new(name="Red_S" ) #allert cube for old statistics
    ROSSO.diffuse_color = (1, 0, 0,0)
    return(1)

def Color_MNG_2():
   #The four values are represented as: [Red, Green, Blue, Alpha]
   ORAN  = bpy.data.materials.new(name="Orange_T"  ) #set new material to variable
   ORAN.diffuse_color = (0.9,0.7,0.01,0)
   GLASS = bpy.data.materials.new(name="Glass_V" ) #set new material to variable
   GLASS.diffuse_color = (0.1, 0.5, 0.7,0)
   return(1)

def Auto_DEL_ALL_OBJ():
   scene = bpy.context.scene
   for object in scene.objects:
    bpy.ops.object.delete()

    
def Stat_Cb_GENERATOR(COLOR_V):
   bpy.ops.mesh.primitive_cube_add( size = 2, location=(-1,(CICLO_0-MEM_D/20)+1, DB_FLR +(OBJ_HGT/2)-1) )
   cube  = bpy.context.selected_objects[0]
   bpy.context.active_object.name = str(OBJ_N + "Allert")
   obj = bpy.context.active_object
   bpy.data.collections['STAT_ALLERT'].objects.link(obj)
   #bpy.data.collections[''STAT_ALLERT'.001'].objects.link(obj)
   bpy.context.scene.collection.objects.unlink(obj)
   bpy.context.active_object.data.materials.append(COLOR_V)#add the material to the object
    
    

Color_d_FL  = 0
DBCONN_d_FL = 0
OBJ_HGT     = 50
DB_FLR      = OBJ_HGT/2 # 25 first floor location - it have to be increased every loop at least of  OBJ_HGT +3
FLR_SEP_C   = 5 # Floors separation distance constant 

Auto_DEL_ALL_OBJ() #Delete preexisting objects

#--------- COLLECTION MANAGEMENT
Collection_MNG_1()
#--------- COLOR MANAGEMENT
#The four values are represented as: [Red, Green, Blue, Alpha]
#Color_d_FL = Color_MNG_1()
ORAN  = bpy.data.materials.new(name="Orange_T"  ) #TEBLE - set new material to variable
ORAN.diffuse_color = (0.98,0.225,0.01,1)
GLASS = bpy.data.materials.new(name="Glass_V" ) #VIEW - set new material to variable
GLASS.diffuse_color = (0.1, 0.5, 0.7,0)
ROSSO = bpy.data.materials.new(name="Red_S" ) #allert cube for old statistics
ROSSO.diffuse_color = (1, 0, 0,0)
VERDE = bpy.data.materials.new(name="Green_S" ) #allert cube for updated statistics
VERDE.diffuse_color = (0, 1, 0,0)
#--------- GESTIONE DB MULTIPLI
DB_LIST = {0 : 'TEST_DB_PAYROLL',1 :'TEST_DB_PAYROLLS_2'}
DB_CNT  = len(DB_LIST)
#--------- CONNECTION
session = DB_CONNECTION_MNG_1()
for i in DB_LIST:
 DB_NAME = DB_LIST[i]
 QUERY = str(" SELECT 'SELECT   '''||TRIM(DATABASENAME)|| '.' || TRIM(TABLENAME) || ''' '   ||  ' AS TABLE_NAME, '''||TRIM(TABLEKIND)|| ''' '   ||  ' AS TABLE_KIND,COUNT(*) AS ROW_COUNT FROM ' || TRIM(DATABASENAME) || '.' || TRIM (TABLENAME) || ' '  FROM DBC.TABLES WHERE TABLEKIND IN ('T','V')  AND DATABASENAME = '")+ DB_NAME + str("' AND TABLENAME<>'TEMP_DB_INFO_V';")
 print(DB_NAME)
 QUERY_2 = []
 print('PREPARING QUERY \n')
 curr_1 =  session.execute(QUERY)
 sql_subq = pd.DataFrame(curr_1.fetchall())
 sql_subq['UNION']='UNION ALL'
 sql_subq1 = sql_subq[sql_subq.columns].astype(str).apply(lambda x: ' '.join(x), axis = 1)
 sql_subq1 =  ' '.join(sql_subq1)
 #print(sql_subq1)
 QUERY_2 = str(sql_subq1)[:int(-9) ]
 QUERY_2 = str('REPLACE VIEW ')+ DB_NAME + str('.TEMP_DB_INFO_V AS (')+ QUERY_2 + str(' );')  #str('ORDER BY 3 ASC ;\n') ##TTRR
 QUERY_3 = ''.join( QUERY_2 )
 #print(QUERY_3)
 print('EXECUTING QUERY \n')
 session.execute(QUERY_3)
 #QUERY_4 = str("SELECT DD.TABLE_NAME , TABLE_KIND,ROW_COUNT,LAST_COLLECT_S , FF.ACTUALSPACE FROM TEST_DB_PAYROLL.TEMP_DB_INFO_V as DD LEFT OUTER JOIN (SELECT DatabaseName ||'.'|| TableName AS TABLE_NAME ,MAX( LastCollectTimeStamp) AS LAST_COLLECT_S FROM DBC.STATSV WHERE StatsId = 0 AND DatabaseName = 'TEST_DB_PAYROLL'      group by 1 ) as ee      ON ee.TABLE_NAME  = DD.TABLE_NAME      LEFT OUTER JOIN (SELECT trim(DatabaseName) ||'.'|| trim(TableName) AS TABLE_NAME           ,SUM(CURRENTPERM)/(1024) AS ACTUALSPACE FROM DBC.TABLESIZE WHERE DATABASENAME = 'TEST_DB_PAYROLL' group by 1 ) AS FF ON FF.TABLE_NAME  = DD.TABLE_NAME order by 3 ;")
 QUERY_4 = str("SELECT DD.TABLE_NAME , TABLE_KIND,ROW_COUNT,LAST_COLLECT_S , FF.ACTUALSPACE FROM ")+ DB_NAME + str(".TEMP_DB_INFO_V as DD LEFT OUTER JOIN (SELECT DatabaseName ||'.'|| TableName AS TABLE_NAME ,MAX( LastCollectTimeStamp) AS LAST_COLLECT_S FROM DBC.STATSV WHERE StatsId = 0 AND DatabaseName = '")+ DB_NAME + str("'      group by 1 ) as ee      ON ee.TABLE_NAME  = DD.TABLE_NAME      LEFT OUTER JOIN (SELECT trim(DatabaseName) ||'.'|| trim(TableName) AS TABLE_NAME ,SUM(CURRENTPERM)/(1024) AS ACTUALSPACE FROM DBC.TABLESIZE WHERE DATABASENAME = '")+ DB_NAME + str("' group by 1 ) AS FF ON FF.TABLE_NAME  = DD.TABLE_NAME order by 3 ;")
 curr_2 = session.execute(QUERY_4)
 sql_data = pd.DataFrame(curr_2.fetchall())
 #print(sql_data)
 sql_data = sql_data.rename(columns={0: 'TABLE_NAME',1:'OBJECT_KIND',2: 'ROW_COUNT'})
 print(sql_data)
 #--------- PREPARING FOR CYCLE
 CICLO_0 = 5
 CICLO_1 = 0
 CICLO_V = -5
 for index, row in sql_data.iterrows():
  #OBJ_N = str(row[0])
  #ROW_C = int(row[2])
  #OBJ_T = str(row[1])
  #STT_D = str(row[3])
  OBJ_N = str(row['TABLE_NAME'])
  ROW_C = int(row['ROW_COUNT'])
  OBJ_T = str(row['OBJECT_KIND'])
  #--- IN CASE OF NO STATISTICS it will be considerate old statistics
  if row[3] == None:
   STT_D = (NOW_V - pd.DateOffset(days=8)).date() #Se non ci sono statistiche e come se fosse statistica vecchia
  else:
   STT_D = row[3].date()
  #---
  NOW_V = pd.to_datetime("now").date()
  MEM_D = float( row[4] if row[4] is not None else -90 )
  if OBJ_T == 'T': # if the object is a Table
   CICLO_0  = CICLO_0+( MEM_D/20)
   bpy.ops.mesh.primitive_cube_add( size = 1, location=( ROW_C/100 ,CICLO_0, DB_FLR ) )
   bpy.ops.transform.resize(value=( ROW_C/OBJ_HGT , MEM_D/10 , OBJ_HGT) )
   cube  = bpy.context.selected_objects[0]
   bpy.context.active_object.name = str(OBJ_N)
   obj = bpy.context.active_object
   #CICLO_1  = CICLO_1  +( ROW_C/100 )
   bpy.data.collections['TABLES'].objects.link(obj)
   #bpy.data.collections['TABLES.001'].objects.link(obj)
   bpy.context.scene.collection.objects.unlink(obj)
   bpy.context.active_object.data.materials.append(ORAN)#add the material to the object
   #-----------------------------NAME MANAGEMENT ------------------------------------
   font_curve = bpy.data.curves.new(type="FONT",name=OBJ_N)
   font_curve.body = "TEBLE :"+OBJ_N.strip()
   str_len = len(font_curve.body.strip())
   font_obj = bpy.data.objects.new("TEXT_" + OBJ_N, font_curve)
   #bpy.ops.transform.resize(value=( ROW_C/50 , MEM_D/10 , 50) )
   font_obj.location = ((- str_len/2) - 3 , CICLO_0-MEM_D/20, DB_FLR +(OBJ_HGT/2)+1)
   bpy.data.collections['TEXT'].objects.link(font_obj)
   #bpy.context.scene.collection.objects.unlink(font_obj)
   #-----------------------------ALLERT OLD STATISTIC -------------------------------
   if str(STT_D)== 'NaT' or STT_D < (NOW_V - pd.DateOffset(days=7)).date():
   #if np.isnat(STT_D) or STT_D < (NOW_V - pd.DateOffset(days=7)).date():
    Stat_Cb_GENERATOR(ROSSO)
   else:
    Stat_Cb_GENERATOR(VERDE)
   print( DB_NAME )
   print( OBJ_N )
   print( STT_D )
    #bpy.ops.mesh.primitive_cube_add( size = 2, location=(-1,(CICLO_0-MEM_D/20)+1, DB_FLR +(OBJ_HGT/2)-1) )
    #cube  = bpy.context.selected_objects[0]
    #bpy.context.active_object.name = str(OBJ_N + "Allert")
    #obj = bpy.context.active_object
    #bpy.data.collections['STAT_ALLERT'].objects.link(obj)
    ##bpy.data.collections[''STAT_ALLERT'.001'].objects.link(obj)
    #bpy.context.scene.collection.objects.unlink(obj)
    #bpy.context.active_object.data.materials.append(ROSSO)#add the material to the object
   #--------------------------------------------------------------------------------------
   CICLO_0  = CICLO_0+( MEM_D/20)+2
   #---------------------------- VIEW MANAGEMENT -----------------------------------------
  if OBJ_T == 'V': # if the object is a View
   bpy.ops.mesh.primitive_cube_add( size = 1, location=( ROW_C/100 ,CICLO_V, DB_FLR ) )
   bpy.ops.transform.resize(value=( ROW_C/OBJ_HGT , MEM_D/100 , OBJ_HGT) )
   cube  = bpy.context.selected_objects[0]
   bpy.context.active_object.name = str(OBJ_N)
   obj = bpy.context.active_object
   bpy.data.collections['VIEW'].objects.link(obj)
   #bpy.data.collections['VIEW.001'].objects.link(obj)
   bpy.context.scene.collection.objects.unlink(obj)
   bpy.context.active_object.data.materials.append(GLASS)
   #-----------------------------------------------------------------
   font_curve = bpy.data.curves.new(type="FONT",name=OBJ_N)
   font_curve.body = "VIEW :"+OBJ_N.strip() 
   str_len = len(font_curve.body.strip())
   font_obj = bpy.data.objects.new("TEXT_" + OBJ_N, font_curve)
   #bpy.ops.transform.resize(value=( ROW_C/50 , MEM_D/10 , 50) )
   font_obj.location = ((- str_len/2) - 3  , CICLO_V, (DB_FLR +(OBJ_HGT/2)+1))
   bpy.data.collections['TEXT'].objects.link(font_obj)
   #bpy.context.scene.collection.objects.unlink(font_obj)
   CICLO_V = CICLO_V -10
 #-- GESTIONE DB MULTIPLI -- -- -- -- -- -- -- -- --
 DB_FLR  =  DB_FLR + (OBJ_HGT*(i+1)) + FLR_SEP_C #preparing for new BD Floor
 #-----------------------------------------------------------------
 print('DONE \n')
 QUERY_5 = str("DROP VIEW TEST_DB_PAYROLL.")+ DB_NAME + str(";")
 session.execute(QUERY_5)
 print( DB_NAME + 'DROPED \n')
   
