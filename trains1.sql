PGDMP                          {            postgres     14.7 (Ubuntu 14.7-1.pgdg22.04+1)     15.2 (Ubuntu 15.2-1.pgdg22.04+1) $    D           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            E           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            F           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            G           1262    13795    postgres    DATABASE     n   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_IN';
    DROP DATABASE postgres;
                postgres    false            H           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    3399                        2615    2200    public    SCHEMA     2   -- *not* creating schema, since initdb creates it
 2   -- *not* dropping schema, since initdb creates it
                postgres    false            I           0    0    SCHEMA public    ACL     Q   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
                   postgres    false    4            �            1259    16460    demo    TABLE     R   CREATE TABLE public.demo (
    start_time date,
    train_id character varying
);
    DROP TABLE public.demo;
       public         heap    postgres    false    4            �            1259    16451    trains    TABLE       CREATE TABLE public.trains (
    train_id integer NOT NULL,
    nominal_odc character varying,
    entraning_station character varying,
    start_time timestamp without time zone,
    detraining_station character varying,
    consignment character varying,
    type character varying
);
    DROP TABLE public.trains;
       public         heap    postgres    false    4            �            1259    16450    master_train_id_seq    SEQUENCE     �   CREATE SEQUENCE public.master_train_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.master_train_id_seq;
       public          postgres    false    4    212            J           0    0    master_train_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.master_train_id_seq OWNED BY public.trains.train_id;
          public          postgres    false    211            �            1259    16420    mst_capacity    TABLE     Z   CREATE TABLE public.mst_capacity (
    station character varying,
    capacity integer
);
     DROP TABLE public.mst_capacity;
       public         heap    postgres    false    4            �            1259    16425    mst_distance    TABLE     w   CREATE TABLE public.mst_distance (
    src character varying,
    dest character varying,
    dist double precision
);
     DROP TABLE public.mst_distance;
       public         heap    postgres    false    4            �            1259    16466    mst_priority    TABLE     l   CREATE TABLE public.mst_priority (
    id integer NOT NULL,
    type character(3),
    priority smallint
);
     DROP TABLE public.mst_priority;
       public         heap    postgres    false    4            �            1259    16465    mst_priority_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mst_priority_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.mst_priority_id_seq;
       public          postgres    false    4    215            K           0    0    mst_priority_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.mst_priority_id_seq OWNED BY public.mst_priority.id;
          public          postgres    false    214            �            1259    16477 	   mst_speed    TABLE     {   CREATE TABLE public.mst_speed (
    type character(1),
    odc character(1),
    speed integer,
    id integer NOT NULL
);
    DROP TABLE public.mst_speed;
       public         heap    postgres    false    4            �            1259    16480    mst_speed_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mst_speed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.mst_speed_id_seq;
       public          postgres    false    4    216            L           0    0    mst_speed_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.mst_speed_id_seq OWNED BY public.mst_speed.id;
          public          postgres    false    217            �            1259    16487 	   train_rpt    VIEW     g  CREATE VIEW public.train_rpt AS
 SELECT a.train_id,
    a.nominal_odc,
    a.type,
    a.entraning_station,
    a.start_time,
    a.detraining_station,
    a.consignment,
    b.speed,
    c.capacity AS d_capacity,
    d.priority,
    e.dist AS distance,
    (a.start_time + ('01:00:00'::interval * (e.dist / (b.speed)::double precision))) AS arrival_time,
    ('01:00:00'::interval * (e.dist / (b.speed)::double precision)) AS travel_time
   FROM ((((public.trains a
     JOIN public.mst_speed b ON ((((a.nominal_odc)::bpchar = b.odc) AND ((a.type)::bpchar = b.type))))
     JOIN public.mst_capacity c ON (((a.detraining_station)::text = (c.station)::text)))
     JOIN public.mst_priority d ON (((a.consignment)::bpchar = d.type)))
     JOIN public.mst_distance e ON ((((a.entraning_station)::text = (e.src)::text) AND ((a.detraining_station)::text = (e.dest)::text))));
    DROP VIEW public.train_rpt;
       public          postgres    false    216    216    216    215    215    212    212    212    212    212    212    212    210    210    210    209    209    4            �            1259    16500    r_trains    VIEW     �  CREATE VIEW public.r_trains AS
 SELECT a.trains,
    a.r_count
   FROM ( SELECT array_agg(train_rpt.train_id) AS trains,
            (array_length(array_agg(train_rpt.train_id), 1) > (array_agg(train_rpt.d_capacity))[1]) AS reschedule,
            (array_length(array_agg(train_rpt.train_id), 1) - (array_agg(train_rpt.d_capacity))[1]) AS r_count
           FROM public.train_rpt
          GROUP BY train_rpt.detraining_station) a
  WHERE a.reschedule;
    DROP VIEW public.r_trains;
       public          postgres    false    218    218    218    4            �           2604    16469    mst_priority id    DEFAULT     r   ALTER TABLE ONLY public.mst_priority ALTER COLUMN id SET DEFAULT nextval('public.mst_priority_id_seq'::regclass);
 >   ALTER TABLE public.mst_priority ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    214    215    215            �           2604    16481    mst_speed id    DEFAULT     l   ALTER TABLE ONLY public.mst_speed ALTER COLUMN id SET DEFAULT nextval('public.mst_speed_id_seq'::regclass);
 ;   ALTER TABLE public.mst_speed ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216            �           2604    16454    trains train_id    DEFAULT     r   ALTER TABLE ONLY public.trains ALTER COLUMN train_id SET DEFAULT nextval('public.master_train_id_seq'::regclass);
 >   ALTER TABLE public.trains ALTER COLUMN train_id DROP DEFAULT;
       public          postgres    false    211    212    212            =          0    16460    demo 
   TABLE DATA           4   COPY public.demo (start_time, train_id) FROM stdin;
    public          postgres    false    213   �)       9          0    16420    mst_capacity 
   TABLE DATA           9   COPY public.mst_capacity (station, capacity) FROM stdin;
    public          postgres    false    209   *       :          0    16425    mst_distance 
   TABLE DATA           7   COPY public.mst_distance (src, dest, dist) FROM stdin;
    public          postgres    false    210   +       ?          0    16466    mst_priority 
   TABLE DATA           :   COPY public.mst_priority (id, type, priority) FROM stdin;
    public          postgres    false    215   �K       @          0    16477 	   mst_speed 
   TABLE DATA           9   COPY public.mst_speed (type, odc, speed, id) FROM stdin;
    public          postgres    false    216   L       <          0    16451    trains 
   TABLE DATA           }   COPY public.trains (train_id, nominal_odc, entraning_station, start_time, detraining_station, consignment, type) FROM stdin;
    public          postgres    false    212   �L       M           0    0    master_train_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.master_train_id_seq', 1, false);
          public          postgres    false    211            N           0    0    mst_priority_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.mst_priority_id_seq', 14, true);
          public          postgres    false    214            O           0    0    mst_speed_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.mst_speed_id_seq', 24, true);
          public          postgres    false    217            �           2606    16459    trains master_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.trains
    ADD CONSTRAINT master_pkey PRIMARY KEY (train_id);
 <   ALTER TABLE ONLY public.trains DROP CONSTRAINT master_pkey;
       public            postgres    false    212            �           2606    16471    mst_priority mst_priority_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.mst_priority
    ADD CONSTRAINT mst_priority_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.mst_priority DROP CONSTRAINT mst_priority_pkey;
       public            postgres    false    215            �           2606    16486    mst_speed mst_speed_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.mst_speed
    ADD CONSTRAINT mst_speed_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.mst_speed DROP CONSTRAINT mst_speed_pkey;
       public            postgres    false    216            =   ]   x�]���0D�3Ԃ#､���C$��h�M-'��J���
�A>'9 �0e�X�k`'�g�~�,(����U�]0SL���徘�\[+�      9   �   x�5P[�!�.�ُ��J`x�i��J{�[4��+{l�<�(h�r3���r���7<#*�+c�CX�e,7�@w'�A���!�\���]�M�%�}/��\v��+��b�6�)�u���W
<\�mE�8N��b1խ���>�$��2F��a�m������R��\�zX�iw�[}�4���P0�CM'�<��@�Yu¸S׻�?Ƙ�?U$      :      x�m]ٲǍ|&?�D����!)Q��"���D���� �D՜��8�kC�B��������_�}���������ݲ������o�[�����z���ݦ��~����g�Ѷ��m/�ۧ�o��s}������o��m�񚮂������>qo���߿���w˵���������?ޝ�������yO��u�������/_����>_��}混����:~��������wǲ}��������������,������_�'�b-��?����ۻ�>�.�C��b�j�����y������~�h_����F���o����Zڏ����?޾����|-G�O��Oo�x�`��k��
~���7|�����ۇ���}}�{�?��]��ZƩ��z�ܯ���?�~��/�~_�|���i��w�â�m�i�3���]��+�u��k��2~����7��a�������o�G�y��6)?Lkm�}{-���C2`�^��pq`[��z4�H�i}�k������Ф����ँ)�ЄxpNN�����xRa��BID���^[�S�a�)�#V���ɇc1e�m4B,���X20�t�u^C����Z{�d�>mΪ�I�m�\uZ���s{�'�q��k���3�my�밮��>��czn�o�܀n�j8;����ނ�L��4,���؞8�iO�\���FEL�\����amI��)���M�>?$ɱ_�������������<^g�� \�m����1����7�k�G]�h���Ti����^�f�ЋAښ4+bs?HsXm��aC[���w�^p�2� ���@s;8��5JrG�O��kS���������;���pXc�\7�-a��o�2���-�8t<Ʀ]b~=A��6�k�`XO�3����v�ھp?�&�<��DiL��?@���|����}���aݮ�}=�������|���X��1�Ț�tܿ����is�>Zk��ܷ�!m�M�c>et����(dx��u]O�H�{����`�����v���%���JR��vP�qW�KJF�6��n��<��?7Py���xI���v���1�x]��y6�,��P�S���}gf�u3�Go@��QPf}�$I��L����ݧy��d�f�boxc�~k4]''@�Rx���W�5	:��s�9";�;t����fS�����j���{�I��_-簨`�YH��z�@��<�e��s��ё��B��b�;������!W׃��~G��&���t[җ��m˽�em�[����p���<rBlC�G�1�0�f4�5�
����#�[�:��P�k�cg$Dj�6�Z�s��|���$�힧�HBm��Z�M�i�������a�	I"y�v���"��Z2h��c:���-6�<�Cl��zW�:�$��1�r��&g�Ҳ��Pl1���i�T�v��6�m��Z} I̩�����j%;L�V}�Q�<^��Ƌ��+NX�w��11�I��������]D������S$:$(20��dtw�J��E�|:2�6¹u!8��=�_�˼;C���'8�as7����m2������"��A� ��9Gl�5ONx�ĵ�fM^��r�2��9"�ѺΠ��ݾB�,��Ǥ̼�ηj���j���m}@�8��l[DPg����:|��[��ߪ�a���3Z�.����ςXtC��̄�s﨨d��1�c�tFȭ�a��̙�ڜ$��O6j�,Z1E8��;��P?h�!|�A��`]Q�q � $َ_z��O�C�����D"�`{4E�-���D@�R]��	��]�A�Dܦŭ�84�qY�d�[��2�I��A�EbZ�t��n9�l?�H�
n���H�>\��~Q�T��%Yw��qЍ�����*R�~A76��)c�纜���s_�-��Z�v�:1��Ʊg�I���1����!���
�z6�QvjoG��F��=1�/��5�����t���?-�2�
49��G�Uڿ � \A��s�:�������\�p�K*��;�����'��h�� u��ƌXrm����$ǜ���!����US������;�vg.���ks
Հ\�3Ǖ��3�5��6�%'��A�(�ns�Ă7�ٜ��7~m�S�F��.`N�� �KN~������\P�c�?�SW�B�`�p�M��'<�H�QҬr �3���`Y �o�G����(@�&D���Y�QZ����cj�ꎾ��L�9��P�bS�2+���:�Jn�pi��>�sm�#+b6����^�������}yM�Aj��ӓ�:u>�{�6���y�9�A�'��Z����V�T���P�q�-e�\h��S��G�����}W�«SǊk[�`��#f�Ry�Yp2��J���4�p��q<E|�ڑ������|�a;����� ߊ"d	bK'�a�Ĵ�O��$�[�qi�Ok��I]���\w�x	k�_gov�lp]Tk�Qs���h�7�f����6B�!v~�o�.�`�Ǭ�2��#3��\0S����;����O�ϵ�'«��=5JC`#X���E�7�5_�S����p�.7.�^�͵>�¾W7.��<5�Ʌ)LUjMeP��x;\l
�| �fRV|`�7���U���F����F)c�.Mb��1HT)��;�d{��B��e�9(^���%\Y���Pה�X,��,F�����J_3�2ϧ��+�0��x'����( Q+���G�B����|��H:G��7�Z��'�)�'����*<Y#��f���R��O�h��o����~�U=�����-���F[}c��-�t(C�(o��1��!Z|a��.<�����c�g�Q�r	�,Lb~d�"Ħ��>���!����`� �B�
�����X<Y"�&�<9,ʽ�cySo���(�J��Q^{Ͷsd��a�ND���1ĳf�rE��u����Q���9Z����h�������f6�8���@��P�ճm,K����w�6���"�[A�)J}Z��T�\�-���Z��Qǒ�����g^eEG(@*D�"Jӄ�C�H2G��3p(A:V8�\����
H2I�R���Rт�,S��$�J�n���$�>�-�p�`��������{k����^�Y�b�k���>&�)�?�+��	�U�<�Z�E�b���pڕq��WO��4�Oʶ�J�r���C��Ǹ{��+�֡�.�I�u����kd_�z��������;Z����w/��q6���R-2�6)��ґ�RP�)A��Q�&����E���]�*W�� �N!7+l�F��D�-4�B�bT�\�3���)XM0J��3*�
�M�ڜ����~]ä)�1�a��2�R�C�Onۄ�Z���֋�����ExY�o(�;�n�kH� ��ϾT4I����C�dйv�fi?�I�d����i���h�f�|�[�ݍ��uU�`��e�(��5�^�7��S�ERY����-��&0��Deh��Ea)�瞡�)Ⱥ:�'Z�	��?*k�,#e�Nȵ&��	�D�6!LO��QJ�*��Lh�&(�VK<R߲n�j�e�,ʘ�>Y�K����̣4�t��P�f��k%��y�b���ڃ/g1��Ɲɴ�n������6�yi=Q��0q.���IK�����f�,P�K�
�l%�Z�!?��ʣ�5?̯��#��v#d�^W!�e���\^�o�J�S0�t��LYQ��X)e��$�2>8RO|�wp2$�yA,�J��M��A
+A���'L�0\*��,q1�&q�B`L�J�yT�*ա��6�83C}έ�Ȝ�r���䋇S��g#���䋑hi�Vj �?��Η	GeZ��C���$�@�8_�Ԁ�k���e�E�/7�ط�4�������ه�7��g�hy�2>�՟�2�T�0��ȝ�XWho��]���Aqʚ�����_C�U�Ř(6Ix$L{�(��S��Z�YhVwFr7A�y���.�ㅊ.�Y/���J\�gX�X�hN�6O�rJ5��#���6�/Hl$�|1��n(�6��T{y\۸3�|�mV��T��AR��b    z���'����/6����Ig����/^t^�
ul�k�T��������<J���;],:j��/���j�\�V
�J5�ى&{CGm}7k3���A	l����r�&Og�.�IQ$��g���&H"�4�	T?�Tp��Pz~��\6��MTnb�&R��XKf��4��:pkX�p�ls���}$�7F'.�m���b&�&�FkI�����������p+��k9�sˣ�o<蹮רY m�)�����5��,���O�H�s���W���`�t-��8�NZS1�qc��t1؅;[��u��@������x�;,��c �����V�j��FEW��ZBT� Qv��E,�ta�o�b8X����H&���Ȗm������$�4�: �-�<��\�\q�$Kɼ4+�'�f�i���b<�7033��7��w]5�;N\�D�,�ogt�2H�Qsy����X�*3��J�e�c�W�@QYvJ�V�~&��
9����s�sx�a�1�M�/B�U�˚@�K��ISv�ܜ��r�������D�$�O�ȏ9��?*F�)3=�7��M$�ʒ���&eGhُ�c9ڋ�O�1�����4O� ː��e�ٲ5J�8�L���<sM�';[#��^;�>��W��z��l�Yv�Ne�ךd�ANQ�ɋ� ����ɖs��p�v��Μ(�t]6��+i�Ŗӡ�����W�vȁ���tj���Z�cJ���5|�}�)����C�z������[ ˻b�:��U��5�T��(���������@3.�Y A�P<� \Q	3����3žfJ��6P%�Qh��!xA��Iq�^�:&�$�����U��ͯi0GE\�ⱗ���:����	������}FV����F�+)�W��Ϥ�~�3�NP�7�K!��~uפC�u�:����=�+��J'٘�^��	�M�y����y�6DM�y�x�</)l�.q��,����+�J�g�@�<
� �s���J]ᨛ�t�Gy�K�y�t9V�5u��$��y�˚6�<�\��y�/ً�yn��h������w�4V(��7�s���qҩU����C�@��[/a����ݝ��y��Y�=?'���,G���q�æ������P�wۃ�S��~�"`�����ԉ���g�"
��R{>�h�z�!���$��\Pu8U�w�+��%�@�\���;K�IugIk`��,�L��j� S�Y����q>hK��-P):����s&G��3�Ug�W1�x9���T��8�$�5U��m���_5�kI�&�m��4g���~�Fqh�7;M����3� �^q��joFʙ럾�W-��j��$�?��ʳw��X|n�(o��K��
��|��G��P��{�5k
TΎ�D����Q�y=�2�9o!S�U�DS�Y�J��5z��Π6�`�;�.�����t��b���z��	�������#�%��#�T_��p�	r��Ò��~�m��dgl�>�Z� �ϦW�dCA�c:= "x�\�Jϻ���ml�ш	[X�l\X�P{u(�3��Z�@>����Sc�ꗙ�n�k��؛k������x�	N>�h��rh¤	�V7I��q}��F��Z��2yA���04IR��MR� �X�HB_�TX��&k��-���p��Ǥ�G���B���_���ú"h@�f�#"ĺM�<� ��@P�.Ro��F�ҧ���6,,��7�z�A;/F]�Q����A7�914!Gl}�
4��7��1z]��������xQfXL�Խ0YvU$?#����;^�#މ�7�(x���P�Co<�A�bo<i@����?�o^�o܆#��;�"	*�+�r�',��<6Ѣ���7��v�x�#���+��3���j
�V8	Њ�R�~�/��D��w��l�l+�sxb9f��)G�t�G!0�V��7{���\��2�8��ٲ��\\97��ʧ8���#��m�&~���Q4G�:�kjHS��#�R�a$�i�#��xW��n���2Q��"+ ��L�M����EB�6QY#�"*Z��a�-�yZ�X�z%�<9��/˳	k��A��������f��`�_'�$%N(q�EC ��:�rN0��t�r=~ӡu
�"'��'$�&d�r"=Iu�N�T	ِ�B�CJN���j�ȉx8�ȗ��(��y�Ek����R	�b?���|��p�__�` T��8�ǝ��|І�(�w:���+ �#x�	�K���o\�#�d�� ��ފHTO��қpQ�ժē
,�˾��7"�\`UE�[R���ZgO�ԍ �ʖb���%eKN�9Z�Hv�x@OI�<�P�0Ƀ�DӃ۰j��*�5�rH"��RJ�Of����@&\��Yj2�9�` ń�o�KE�����jK`��]��|m�h�z D�4�13�i���V	��i �4���.� @*:Ľh�ixA`�}��h� /}^�kW��xY�X�է�k����W(#Ҵ� ��!� �y���	p>�E

0w�Vpz	'���^�~��&0�w�M����'�J��}�}������R�o�j��y���VT��C��R�C=��\y~��W����M)=�����B�)]�F��Ә�v��{}� |�,�^O0I��v��L��BE< \|��h�E	\� Y�kp�1p�G�V]��	�=P�]cCPi*�H�>�Uār��j�

Z���&a��V78Ó�j4"s�dk"�$�jD�x��R�AZ?�$�������%����ҁW��d�xO�va�$c�y��򻶽�ݧr�}�Ժ�(}Ȏ���$ͤ�)j�Fj�]YI�Z|�R2��	����#��&��p�p�.0��S���«��n��p9\�AZxR�W�$hN����
qy��_O�Ê��B-j��$k��R�j<*�Z��OYZ�0OUp�\k�#t�U�q��㌚�"�vkD-,A���$O^"�n=	F1�hp0�nV�}��a�J�t�JU�P�!�ٻBJ9���U�>�y�T�1L$5�%gk�]r�3���|;�'��3e�F�X�i��B&�2O|���Ȣ|=2�&>�D,�!�f�Op����� ���Z'*�ě�ċ<��F\�����*����P�]sX�Z�jEP��Wڲ+��d����\6D-W[z���1_��-�wd��&L�j��#˔��� ��&'B���8�CƔ���!��g�0١d�>E63ׁ�|��u^�n{��Қ�?�1�xHҩ��@�9�
���x%Y"1�����
������|E�R��	S��pq���gX���� (\��jIgp-T�bn��ě�Y\
��f�,�º����֯ +��BQ�T��������z�'�5�F%T���1g�f�$��j�������sл:��SV��`Z�3�?����W�{��C5ˌ��,Z�˷��������IA����������6�o�� �7<��hq��Ʀ������{ë}���o�%��[<攠��7k��{1��#>@����u
�m˻�춼6\�K\�͟6�u�7juഡH�zb1k�t�P�E�?����5$>ك�t��k8˫���'���D
�P$���j��������!fшu��B6;A�F���� �Ӭ��[���#۾, h?k�,���������i��q҉Mޏ\�����7I;{��M�8�+�M�3�uY��a��_��(/�5I��ɧ&�ښ�s�%u,�G<����-�&��\��C�)����jp�n�z��7{�UŁ.?]αN�	H;��v��&J{��fWh����f��A����Y5��¡W,Ɍ3�A�Y�B��&E��+��}H�)Q�1O��x�����ְ� #��5��b���R6�#m�{%�]*��B6��2�:6���U��
 ��?�d�QÆW�!"��, U��a� U�����PQ�H��5�� �   ���k@�vo��b�e-&���&�H�[p� �[�E������� /lb�P��B\6�j9Ό���߭��#�*��pn��"Ǎc�����E���D��� " ;Ʊ��-"|����M�&�&8f��y��۩���y���� ��2l      ?   P   x�%�;
�0@���)rq��QA�`!��?�aS�(�9T<��̊5�f0f��0;N��Iђ%Gys<SN�����W�n      @      x�-�I�0C�5y�B��$˴=@:oz�s���{�?a���np8�B� M�b:o�!��2^����W�	ٸI�K�H�l�&U�����Φnk�H;����M���3��Z�K����/M�ut~O$�5#�      <   +  x���Qn�0�gs
.�)-�LA�BS`U�I��-f#P65��x���5��N�,�-h�����cԅR����I��+T0D���
����;��0;�;D��·�_�'���w̏�a0�Q����AZ���=z;Ͷ����1�䭡�8�f�q�qI�n��	7��>{}����,�<8s���8��\Ԟ����:����-)	f��C|0����i��T-���۩��QR�nZ����n�c��'C�^�ǌ��dnue�!�,J\�)����o�[����V9e-���|���(v�}     