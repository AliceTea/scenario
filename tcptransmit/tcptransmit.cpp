#include <iostream>
#include <ifstream>
#include <string>
#include <sys/types.h>
#include <sys/socket.h>
using namespace std;

int getret(char* file){
	ifstream ifile(file,ios::in);
	ifile.open(ios_base::_Openprot);
	if(ifile.is_open()){
		
		//obtain source port and des IP and des port
		int s_port,d_port;
		string d_ip;
		ifile>>s_port>>d_ip>>d_port;
		
		//connect to server 
		int sockfd;
		struct sockaddr_in my_addr;

		sockfd = socket(AF_INET,SOCK_STREAM,0);

		my_addr.sin_family = AF_INET;
		my_addr.sin_port = htons(s_port);
		my_addr.sin_addr.s_addr=inet_addr(d_ip);
		bzero(&(my_addr.sin_zero),8);

		bind(sockfd,(struct sockaddr *)&my_addr,sizeof(struct sockaddr));


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
