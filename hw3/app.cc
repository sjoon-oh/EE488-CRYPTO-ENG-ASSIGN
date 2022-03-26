#include <cstdio>
#include <cstdint>

namespace hw_3 {
    class Node {
    private:
        uint16_t    n_id;   // Node ID
        uint16_t    n_val;  // Node Internal Value  
        int32_t     c_id;   // Cycle ID

        bool        ready;  // Is the calc done?

    public:
        Node();
        Node(uint16_t, uint16_t);

        uint16_t set_id() = delete;
        uint16_t set_val();

        uint16_t get_id();
        uint16_t get_val();



    };
}

hw_3::Node::Node() {
    this->n_id = this->n_val = 0;
    this->c_id = -1;

    this->ready = false;
}

hw_3::Node::Node(uint16_t argId, uint16_t argVal)
    : n_id(argId), n_val(argVal), c_id(-1), ready(false) {

}




int main(char** argc, int argv) {

    


    return 0;
}