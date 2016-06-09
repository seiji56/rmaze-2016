#include <SFML/Graphics.hpp>
#ifdef __linux__
#include <X11/Xlib.h>
#endif // __linux

#include "simulator.hpp"

sim_logic simulation;

bool has_size_changed = false;

void render_t(sf::RenderWindow *window)
{
    window->setActive(true);

    // Temporary 'screen'
    sf::RenderTexture physical_draw;
    physical_draw.create(window->getSize().x/2, window->getSize().y);

    while(window->isOpen())
    {
        if (has_size_changed)
        {
            physical_draw.create(window->getSize().x/2, window->getSize().y);
            has_size_changed = false;
        }

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
    case sf::Event::Resized:
        {
            has_size_changed = true;
            sf::View oldview = window->getView();
            oldview.setSize(window->getSize().x, window->getSize().y);
            oldview.setCenter(window->getSize().x/2, window->getSize().y/2);
            window->setView(oldview);
        }
        break;
    default:
        break;
    }
}

void sim_test()
{
}

int main()
{
#ifdef __linux__// Call XInitThreads in case of linux compilation
    XInitThreads();
#endif // __linux__

    sf::RenderWindow window(sf::VideoMode(800, 600), "Logic Simulator");
    window.setActive(false);

    // Load map and other things
    try
    {
        simulation.load_map("map.map");
    }
    catch (int error)
    {
        printf("Error %d\n", error);
        exit(error);
    }

    // Start Threads

    sf::Thread rendering_thread(&render_t, &window);

    rendering_thread.launch();
    sf::Thread sim_teste(&sim_test);

    sim_teste.launch();
    // Event loop

    while(window.isOpen())
    {
        sf::Event evn;
        while(window.pollEvent(evn))
        {
            handleEvn(evn, &window);
        }
    }

    sim_teste.terminate();
    rendering_thread.wait();
}
