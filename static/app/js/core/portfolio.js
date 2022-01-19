function portfolioState() {
    return {
        repos: [
            {
                name: 'NestJS Microservices',
                description: 'Microservices built by using NestJS. It contains various services like api gateway, mail service, user management service and a store service for managing product inventory. This entire project follows CI/CD approach using docker, ansible and github workflows.',
                url: 'https://github.com/ReddyPrashanth/nestjs-microservices'
            },
            {
                name: 'Microservices Admin Dashboard',
                description: 'Admin Interface built by React JS. It provides an intuitive interface to manage users and products. It uses redux for state management across multiple UI components.',
                url: 'https://github.com/ReddyPrashanth/admin-dashboard'
            },
            {
                name: 'Django Blog Application',
                description: 'This is a blog application build by django framework. This site is built by using django, tailwind css and alpine js. Current website is a live version of this project.',
                url: 'https://github.com/ReddyPrashanth/django-project'
            },
            {
                name: 'Configuration Mgmt Using Ansible Roles',
                description: 'This repository provides configuration management for jenkins and nginx on Linux/Debian distribution. It uses roles for each task to be executed on operating system.',
                url: 'https://github.com/ReddyPrashanth/ansible-roles'
            },
            {
                name: 'Laravel Cart Api',
                description: 'This is a simple ecommerce api to explore laravel 8 features. Laravel is a PHP based web framework.',
                url: 'https://github.com/ReddyPrashanth/shopping-cart'
            },
            {
                name: 'Vue JS Cart Client',
                description: 'An user interface for shopping cart Laravel API which allows users to add products to shopping cart and complete the purchase transaction.',
                url: 'https://github.com/ReddyPrashanth/shopping-cart-client'
            },
        ]
    }
}