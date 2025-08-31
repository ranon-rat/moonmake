#include <iostream>
#include <thread>
#include <chrono>


void dance(int iterations,int delay){

    for(int i=0;i<iterations;i++){
        std::cout<<"♪┏(・o･)┛♪┗ ( ･o･) ┓♪\r";
        std::this_thread::sleep_for(std::chrono::milliseconds(delay));
        std::cout<<"┗ ( ･o･) ┓♪┏(・o･)┛♪\r";
        
        std::this_thread::sleep_for(std::chrono::milliseconds(delay));
    }
    std::cout<<std::endl;
}