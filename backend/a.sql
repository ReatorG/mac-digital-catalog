DELETE FROM artists
WHERE id = 5;

DELETE FROM ARTWORKS
WHERE id = 21;

UPDATE FROM ARTWORKS
WHERE id = 11

SELECT * FROM ARTISTS;
SELECT * FROM ARTWORKS;

INSERT INTO artists
(name, surname, birth_date, image_url, gender, biography)
VALUES
(
    'Mariella',
    'Agois',
    '1956-01-21',
    'https://elcomercio.pe/resizer/LQg9KtcfuQip9Pmk2jiBsm0QqzU=/1200x1200/smart/filters:format(jpeg):quality(75)/arc-anglerfish-arc2-prod-elcomercio.s3.amazonaws.com/public/JGLPZHEXIRFHZBSV4TQBUIUVWQ.jpg',
    'female',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sagittis nunc ut auctor aliquet. Nunc auctor ultricies nisi, vitae commodo ipsum maximus a. Quisque et tempor nunc. Suspendisse potenti. Integer purus libero, ultrices at aliquam et, luctus et justo. Proin suscipit mattis dictum. In ante neque, efficitur eget dui ut, consectetur scelerisque massa. Duis et lectus metus. Ut semper nisi sed justo viverra fringilla. Quisque neque leo, tristique ac accumsan eu, finibus vitae tortor. Aliquam sagittis venenatis lectus quis tincidunt. Aliquam iaculis, sem et molestie faucibus, augue ante iaculis lorem, at vulputate dolor nibh eu nisi.
	
	Suspendisse id scelerisque ex. Sed ut dui nibh. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed egestas maximus rutrum. Nullam ut sem in tellus accumsan convallis quis et felis. Integer sapien est, sodales ut mi nec, tristique ullamcorper nulla. Maecenas egestas id metus eu lacinia. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ullamcorper dui ac ligula porta, vitae vulputate ligula malesuada.
	
	Nam sed magna a risus elementum bibendum lobortis id est. Donec sit amet est in metus viverra porta. Sed quis aliquet magna, et volutpat neque. Ut nec odio eget urna aliquet mattis. Maecenas nibh turpis, sodales et enim a, venenatis auctor ligula. Fusce mollis leo risus, eu volutpat metus suscipit ut. Vivamus mollis enim non ante aliquam iaculis. Etiam tempor justo sem, sed mattis massa hendrerit non. Ut tellus risus, ornare et commodo in, sodales nec eros.'
);



INSERT INTO artworks
(artist_id, title, series, year, technique, materials, location, image_url, description, on_display)
VALUES
(
    14,
    'Pliegue 45',
    ' - ',
    2021,
    'Acrílico sobre lienzo',
    'Lienzo',
    'Museo Arte Contemporaneo',
    'https://catalogo.maclima.pe/wp-content/uploads/2021/11/Pliegue-45-Mariella-Agois-Coleccion-MAC-Lima-scaled.jpg',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam sagittis nunc ut auctor aliquet. Nunc auctor ultricies nisi, vitae commodo ipsum maximus a. Quisque et tempor nunc. Suspendisse potenti. Integer purus libero, ultrices at aliquam et, luctus et justo. Proin suscipit mattis dictum. In ante neque, efficitur eget dui ut, consectetur scelerisque massa. Duis et lectus metus. Ut semper nisi sed justo viverra fringilla. Quisque neque leo, tristique ac accumsan eu, finibus vitae tortor. Aliquam sagittis venenatis lectus quis tincidunt. Aliquam iaculis, sem et molestie faucibus, augue ante iaculis lorem, at vulputate dolor nibh eu nisi.
	
	Suspendisse id scelerisque ex. Sed ut dui nibh. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed egestas maximus rutrum. Nullam ut sem in tellus accumsan convallis quis et felis. Integer sapien est, sodales ut mi nec, tristique ullamcorper nulla. Maecenas egestas id metus eu lacinia. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ullamcorper dui ac ligula porta, vitae vulputate ligula malesuada.
	
	Nam sed magna a risus elementum bibendum lobortis id est. Donec sit amet est in metus viverra porta. Sed quis aliquet magna, et volutpat neque. Ut nec odio eget urna aliquet mattis. Maecenas nibh turpis, sodales et enim a, venenatis auctor ligula. Fusce mollis leo risus, eu volutpat metus suscipit ut. Vivamus mollis enim non ante aliquam iaculis. Etiam tempor justo sem, sed mattis massa hendrerit non. Ut tellus risus, ornare et commodo in, sodales nec eros.',
    TRUE
);