# Project Context

Description: Chat multiempresa de atención al cliente que unifica WhatsApp, Facebook Messenger, Instagram, Telegram, Discord y correo electrónico en una sola bandeja por empresa.
Development type: both
Application type: web
Environments in scope: development, local, production

Chat Multi Empresa para que los usuarios de Meta (WhatsApp, Facebook, Instagram) y los usuarios de otras aplicaciones como Telegram o Discord o correos electrónicos se puedan comunicar por atención al cliente con la empresa respectiva que desean o tienen el medio de contacto.

uwuChat es una plataforma SaaS multiempresa (multi-tenant). Cada empresa registra sus canales (número de WhatsApp Business, página de Facebook, cuenta de Instagram, bot de Telegram, servidor/bot de Discord y buzones de correo) y sus agentes de atención. Los mensajes entrantes de cualquier canal llegan por webhooks o por sondeo (IMAP), se normalizan a un modelo común de conversación y se enrutan a la empresa dueña del canal. Los agentes responden desde una bandeja unificada web y la respuesta sale por el mismo canal por el que escribió el cliente.
