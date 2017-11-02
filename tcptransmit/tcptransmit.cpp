#include<iostream>
#include<unp>
#include<ifstream>
#include<string>
using namespace std;

int getret(char* file){
	ifstream ifile(file,ios::in);
	ifile.open(ios_base::_Openprot);
	if(ifile.is_open()){
		
		//obtain source port and des IP and des port
		int s_port,d_port;
		string d_ip;
		ifile>>s_port>>d_ip>>d_port;
		
		//connect
	    	
		
		//clock interrupt 
		

		ifile.close();
	}
	return 0;
}

int main(int args,char *argv[]){
	if(args==0){
		cout<<"Need arguements"<<endl;
	}
	else if(args==1){
		getret(argv);
	}
	else{
		cout<<"illegde arguement"<<endl;
	}
	return 0;
}
