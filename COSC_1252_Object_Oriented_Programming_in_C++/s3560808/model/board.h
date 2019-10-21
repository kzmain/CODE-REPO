#include <memory>
#include "model.h"
namespace draughts
{
    namespace model
    {
        class board : public model{
            int width;
            int height;
            
            static std::unique_ptr<board> instance;
        public:
            board(void):
                width(8),
                height(8)
            {}
            board(int width, int height):
                width(width),
                height(height)
            {}
            virtual ~board(){};
            static board * get_instance(void);
            int get_width(void) noexcept;
            int get_height(void) noexcept;
            void delete_instance(void);
        };
    }
}