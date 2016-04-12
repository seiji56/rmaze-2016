#include <SFML/Graphics.hpp>

void render_t(sf::RenderWindow *window)
{
    while(window->isOpen())
    {
        window->clear();
        //Drawing code
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
    sf::RenderWindow window(sf::VideoMode(800, 600), "Logic Simulator");
    //Start Threads
    sf::Thread rendering_thread(render_t, &window);

    rendering_thread.launch();

    //Event loop

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
