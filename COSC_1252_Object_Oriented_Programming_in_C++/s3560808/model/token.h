#include "model.h"

namespace draughts
{
    namespace model
    {
        enum class token_type{
            normal,crown
        };
        class token{
        public:
            int x;
            int y;
            draughts::model::token_type type = token_type::normal;
            token(int x_value, int y_value):x(x_value),y(y_value),type(token_type::normal){}
            token(int x_value, int y_value, token_type type):x(x_value),y(y_value),type(token_type::crown){}
            int get_x_value(void);
            int get_y_value(void);
            draughts::model::token_type get_type(void);
            virtual ~token(void){};
        };
    }
}