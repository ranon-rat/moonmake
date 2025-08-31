#include <vector>
#include <iostream>

template <typename T>
void ShowMeVectorMeEatBanana(const std::vector<T>& v){
    for(auto i : v)
        std::cout<<i<<" ";
    std::cout<<"\n";
}