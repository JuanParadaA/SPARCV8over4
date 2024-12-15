#BACKEND MEM#########################
import array
import uctypes
import ure
import json

memory={}

struct_32 = {
    "value": uctypes.UINT32 | 0  # UINT32 es un entero sin signo de 32 bits, y 0 es el offset en la estructura
}

def get_uctype(address):
    if  address not in memory:
        memory[address]=uctypes.struct(address, struct_32)
    return memory[address]
    
def read_memory(address,rd):
    assert address % 4 == 0, f"The address {address} is not divisible by 4."
    print('read_memory',address)
    return get_uctype(address).value

def write_memory(address,data):
    assert address % 4 == 0, f"The address {address} is not divisible by 4."
    print( 'write_memory',address,data)
    get_uctype(address).value=data
     
def malloc(num_bytes,rd):
    assert num_bytes % 4 == 0, f"The number {num_bytes} is not divisible by 4."
    buff_0 = array.array('b', (10+_ for _ in range(num_bytes)))
    dir0 = uctypes.addressof(buff_0)
    print('malloc',num_bytes,dir0,type(dir0))
    for address in range(dir0,dir0+num_bytes,4):
        write_memory(address,0)
    
    return dir0

def str2tuple(txt):
    print('str2tuple',txt)
    return txt.strip("()[}").replace('%2C',',').split(",")


def api( request_str):

    print('api_in')#,request_str)
    match = ure.search(r'GET /api\?([^\s]+) HTTP', request_str)
    response_dir={}
    if match:
        query_string = match.group(1)
        params = query_string.split('&')
        json_data = {}
        for param in params:
            key, value = param.split('=')
            json_data[key] = value
        
        print("Received JSON data:")
        dat_r=json.dumps(json_data)
        print(json_data)  # Pretty print the JSON data
        for key,val in json_data.items():
            print('dic',key,val)
            if key=='malloc':
                numb,rd = str2tuple(val)
                numb=int(numb)
                address=malloc(numb,rd)
                for addr_i in range(address,address+numb,4):
                    response_dir[addr_i]=0
                response_dir[rd]=address
            elif key=='write_memory':
                
                #cleaned_string = val.strip("()")
                #addr,dat = cleaned_string.split(",")
                addr,dat = str2tuple(val)
                addr=int(addr)
                dat=int(dat)
                write_memory(addr,dat)
                response_dir[addr]=dat
            elif key=='read_memory':
                addr,rd = str2tuple(val)
                addr=int(addr)
                dat=read_memory(addr,rd)
                response_dir[addr]=dat
                response_dir[rd]=dat

    response_json = json.dumps(response_dir)
    #print(response_json)
    response_str=('HTTP/1.1 200 OK\r\n'
            + 'Content-Type: application/json\r\n'
            + 'Connection: close\r\n\r\n'
            + response_json)
    print('api_out',response_str)
    return (response_str )


     
