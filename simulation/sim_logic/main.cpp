#include <SFML/Graphics.hpp>
#ifdef __linux__
#include <X11/Xlib.h>
#endif // __linux

#include "simulator.hpp"

sim_logic simulation;

void render_t(sf::RenderWindow *window)
{
    window->setActive(true);

    // Temporary 'screen'
    sf::RenderTexture physical_draw;
    physical_draw.create(window->getSize().x/2, window->getSize().y/2);

    while(window->isOpen())
    {
        window->clear();
        simulation.draw_phys_map(&physical_draw);

        window->draw(sf::Sprite(physical_draw.getTexture()));

        // Drawing code
        window->display();
    }
}

void handleEvn(sf::Event &evn, sf::RenderWindow* window)
{
    switch(evn.type)
    {
    case sf::Event::Closed:
        window->close();
        break;
    default:
        break;
    }
}

int main()
{
#ifdef __linux__// Call XInitThreads in case of linux compilation
    XInitThreads();
#endif // __linux__

    sf::RenderWindow window(sf::VideoMode(800, 600), "Logic Simulator");
    window.setActive(false);

    // Load map and other things

    simulation.load_map("map.map");

    // Start Threads

    sf::Thread rendering_thread(&render_t, &window);

    rendering_thread.launch();

    // Event loop

    while(window.isOpen())
    {
        sf::Event evn;
        while(window.pollEvent(evn))
        {
            handleEvn(evn, &window);
        }
    }

    rendering_thread.wait();
}
