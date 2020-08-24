import teradata
import teradatasql
import pandas as pd
import bpy
#RUN BLENDER AS ADMINISTRATOR !!!!
 
print ( '\n INIZIO CONNESSIONE \n' )
host,username,password = '000.000.00.000','User_id', 'user_pw'
udaExec = teradata.UdaExec (appName="#D_data_dictionary", version="1.0",logConsole=False) 
session = udaExec.connect(method="odbc", system=host,username="dbc", password="dbc");
print( ' \n CONNESSIONE EFFETTUATA \n' )
                 
#you will need to modyfy all the DATABASE NAME IN THE WHERE CONDITION
#query =" SELECT 'SELECT   '''||TRIM(DATABASENAME)|| '.' || TRIM(TABLENAME) || ''' '   ||  ' AS TABLE_NAME,COUNT(*) AS ROW_COUNT FROM ' || TRIM(DATABASENAME) || '.' || TRIM (TABLENAME) || ' '  FROM DBC.TABLES WHERE TABLEKIND IN ('T','V')  AND DATABASENAME = 'DATABASE_NAEM';  "  
query =" SELECT 'SELECT   '''||TRIM(DATABASENAME)|| '.' || TRIM(TABLENAME) || ''' '   ||  ' AS TABLE_NAME, '''||TRIM(TABLEKIND)|| ''' '   ||  ' AS TABLE_KIND,COUNT(*) AS ROW_COUNT FROM ' || TRIM(DATABASENAME) || '.' || TRIM (TABLENAME) || ' '  FROM DBC.TABLES WHERE TABLEKIND IN ('T','V')  AND DATABASENAME = 'DATABASE_NAEM';"  

QUERY_2 = [] 
print('\n PREPARING QUERY \n') 
curr_1 =  session.execute(query)
sql_subq = pd.DataFrame(curr_1.fetchall())
sql_subq['UNION']='UNION ALL'
sql_subq1 = sql_subq[sql_subq.columns].astype(str).apply(lambda x: ' '.join(x), axis = 1)
sql_subq1 =  ' '.join(sql_subq1)

QUERY_2 =  str(sql_subq1)[:int(-9) ]
QUERY_2 = QUERY_2 + str('ORDER BY 3 ASC ;\n')
print(QUERY_2)
 

#print('--------------------------------------------------------')
QUERY_3 = ''.join( QUERY_2 )
#print(QUERY_3)
#print('--------------------------------------------------------')

print('\n EXECUTING QUERY \n') 
print('\n IN THE DWH THE FOLLOWING TABLES ARE AVAILABLE,\n YOU WILL FINDE THE RELATED ROWCOUNT ON THE SIDE  \n') 

curr_2 = session.execute(QUERY_3)
sql_data = pd.DataFrame(curr_2.fetchall())
#print(sql_data)
#print('\n\n\n')
sql_data = sql_data.rename(columns={0: 'TABLE_NAME',1:'OBJECT_KIND',2: 'ROW_COUNT'})
print(sql_data)
#print('\n\n\n')
#for col in sql_data.columns: 
#   print(col) 
    
    
#convert table in list of 2 dictionary    
#print('\n\n\n')
fg=sql_data.set_index('TABLE_NAME').T.to_dict('ROW_COUNT') 
#print(fg)
   
TABLE_LIST  = fg[0].keys()
OBJECTS_K_L = fg[0] #object kind list
OBJECTS_N_L = fg[1] #row count list 
#print(TABLE_LIST)
#print(OBJECTS_K_L)
#print('\n')
#print(OBJECTS_N_L)

#--------- COLLECTION MANAGEMENT -- To assign table and Views in 2 different blender collection

collection_T = bpy.data.collections.new('TABLES')
bpy.context.scene.collection.children.link(collection_T)
collection_V = bpy.data.collections.new('VIES')
bpy.context.scene.collection.children.link(collection_V)


#--------- COLOR MANAGEMENT 
#Views and Tables will have 2 different colors
#The four values are represented as: [Red, Green, Blue, Alpha]

ORAN  = bpy.data.materials.new(name="Orange_T"  ) #set new material to variable
ORAN.diffuse_color = (0.9,0.7,0.01,0) 
GLASS = bpy.data.materials.new(name="Glass_V" ) #set new material to variable
GLASS.diffuse_color = (0.1, 0.5, 0.7,0) 

#CREATE THE CUBES 
CICLO = 0
for a in TABLE_LIST:
    print(a)
    ROW_C = int(OBJECTS_N_L[a])
    OBJ_T = str(OBJECTS_K_L[a])
    bpy.ops.mesh.primitive_cube_add( size = (ROW_C/100), location=((0 + CICLO , (0) , 0) ) )
    cube  = bpy.context.selected_objects[0]
    bpy.context.active_object.name = str(a)
    CICLO = CICLO +(( (ROW_C/100) + 1)* 2)
    obj = bpy.context.active_object
    #Assing Object to different collections and Colors based on them nature ( Views or Tables )
    if OBJ_T == 'T': # if the object is a Table 
     #!! Pay attention before run the script that no Collections with similar names are already been created
     bpy.data.collections['TABLES'].objects.link(obj)
     #bpy.data.collections['TABLES.001'].objects.link(obj)
     bpy.context.scene.collection.objects.unlink(obj)
     bpy.context.active_object.data.materials.append(ORAN) #add the material to the object
    if OBJ_T == 'V': # if the object is a View 
     bpy.data.collections['VIES'].objects.link(obj)
     #bpy.data.collections['VIES.001'].objects.link(obj)
     bpy.context.scene.collection.objects.unlink(obj)
     bpy.context.active_object.data.materials.append(GLASS) #add the material to the object
 