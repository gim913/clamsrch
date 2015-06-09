# Changes #

These are different changes that I've made to original signsrch.sig.

I haven't checked every, single signature, only those that "seemed" somehow suspicious.



## fixed/changed ##

  * `ADPCM index table (step variation)`
  * `Boucher randgen4 - fixed`
  * `Bzip2 BZ2_rNums - fixed`
  * `G726 40kbit/s 5bits per sample table`
  * `ICE ice_pbox -> fix, rename "ICE (block cipher) ice_pbox"`
  * `liba52 bndtab -> "AC3 starting frequency coeeficients bndtab (avcodec / liba52)"`
  * `libavcodec dpcm interplay_delta_table`
  * `libavcodec DV dv_audio_shuffle525`
  * `libavcodec DV dv_audio_shuffle625`
  * `libavformat ff_mxf_data_definition_uls`
  * `libdjvu GPixmap dither table`
  * `LZRW1 test`
  * `mp3lib intwinbase_MMX -> fixed`
  * `mp3lib intwinbase -> fixed`
  * `MS ADPCM AdaptationTable`
  * `Nsis archive signature`
  * `Phelix`
  * `pred_max_bands_tbl -> "AAC pred_max_bands_tbl (avcodec)"`
  * `PSX VAG depack`
  * `sfb_16_128 -> "MPEG-2 NBC sfb_16_128 (avcodec / faad)"`
  * `sfb_24_128 -> "MPEG-2 NBC sfb_24_128 (avcodec / faad)"`
  * `sfb_48_128 -> "MPEG-2 NBC sfb_48_128 (avcodec / faad)"`
  * `sfb_8_128  -> "MPEG-2 NBC sfb_8_128 (avcodec / faad)"`
  * `sfb_96_128 and sfb_64_128 -> "MPEG-2 NBC sfb_96_128 and sfb_64_128 (avcodec / faad)"`
  * `sol_table_old / sol_table_new`
  * `T264_cabac_range_lps -> Binary arithmetic decoder  LPSTable / T264_cabac_range_lps`
  * `tns_max_bands_tbl -> "TNS filter tnsMaxBands (combined)"`
  * `UPX miniacc`
  * `Yamaha ADPCM diff lookup table`
  * `Yamaha ADPCM index table`
  * `zdeflate_lengthCodes`
  * `zinflate_distanceExtraBits`
  * `zinflate_distanceStarts`
  * `zinflate_lengthExtraBits`
  * `zinflate_lengthStarts`

## removed ##
  * `DEAL`

## added (during checking) ##
  * `bsynz kexc table float`
  * `ElGamal public key encryption (qbits)`
  * `id3tag genre_alpha_map`
  * `Inverse Modified DCT pm64 (liba52)`
  * `libmpdemux tivo Series2AudioWithPTS`
  * `libskba asn1 yycheck`
  * `Serpent crypto FPTable`
  * `Serpent crypto IPTable`
  * `TNS filter long SSR tnsMaxBandsLong`
  * `TNS filter long tns_max_bands_1024 (avcodec)`
  * `TNS filter short SSR tnsMaxBandsShort`
  * `TNS filter short tns_max_bands_128 (avcodec)`

## Unified sigs ##
  * `padding used in hashing algorithms (0x80 0 ... 0)`
  * `G.721 _fitab`
  * `G.723_24 _fitab`
  * `G.723_40 _fitab`
  * `in_cube AFC decoder (ngc_afc_decoder)`
  * `power2 table`
  * `MBC2`

## checked ##
  * `(N)SA LPC-10 Voice Coder TAU`
  * `AAC escAssignment[MAX_ELEMENTS][NR_OF_ASSIGNMENT_SCHEMES] -> renamed "MPEG AAC Fraunhofer escAssignment"`
  * `BICOM bialib sufftree.cpp dini`
  * `Boucher randgen5`
  * `Creative ADPCM table`
  * `ElGamal public key encryption`
  * `Electronic Arts ADPCM table`
  * `GSM table gsm_MAC`
  * `GSM table gsm_MIC`
  * `HAM84 DAC tab`
  * `Huffman book1   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book10  -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book11  -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book2   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book3   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book4   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book5   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book6   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book7   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book8   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman book9   -> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman bookRvlc-> prefix "MPEG-2 NBC Fraunhofer"`
  * `Huffman booksc1 -> prefix "MPEG-2 NBC Fraunhofer"`
  * `ICE ice_smod -> "ICE (block cipher) ice_smod"`
  * `ICE ice_sxor`
  * `ICE ice_sxor -> "ICE (block cipher) ice_sxor"`
  * `Kasumi S7`
  * `LD-CELP G.728 cb_gain_mid`
  * `LZO 1x_999 compress level`
  * `LZSS (N 4096, F 18, T 2)`
  * `Lame freq_map`
  * `Little CMS isotempdata - 4 doubles`
  * `MPEG-4 mcc gmmtable -> rnamed "MPEG-4 ALS decoder mcc_weightings"`
  * `Macromedia Flash SWF ADPCM table`
  * `PPMZ2 counts`
  * `PSX VAG CD-ROM XA ADPCM table`
  * `Smacker sizetable`
  * `Squash table used in PAQ7 compression`
  * `TIFF mkg3states TermB`
  * `Torque Huffman frequency table`
  * `Zlib base_dist`
  * `__popcount_tab (compression?) -> "Bit count 256 __popcount_tab (popullation count)"`
  * `anti-debug: PeID GenOEP Spoofing`
  * `anti-debug: PeID OEP Signature Spoofing`
  * `anti-debug: RDG OEP Signature Spoofing`
  * `bsynz kexc table`
  * `bsynz kexc table (float)`
  * `epTool punctbl`
  * `len_table (from h264) -> renamed "meaningful bits table bs_write_ue (from x264)"`
  * `liba52 hthtab`
  * `liba52 pm128 -> "Inverse Modified DCT pm128 (liba52)"`
  * `libavcodec DV dv_iweight_248`
  * `libavcodec DV dv_iweight_88`
  * `libavcodec DV muxer/demuxer dv_aaux_packs_dist`
  * `libavcodec On2 Vp3 predictor_transform`
  * `libavcodec VC-1 vc1_ac_tables`
  * `libavcodec Video XL delta`
  * `libavcodec asus v1/v2 ac_ccp_tab`
  * `libavcodec asus v1/v2 asv2_level_tab`
  * `libavcodec asus v1/v2 ccp_tab`
  * `libavcodec asus v1/v2 dc_ccp_tab`
  * `libavcodec dpcm sol_table_16`
  * `libavcodec ff_mlp_huffman_tables`
  * `libavcodec h261_tcoeff_vlc`
  * `libavcodec h263 inter_vlc`
  * `libavcodec h263 intra_vlc_aic`
  * `libavcodec indeo ir2_codes`
  * `libavcodec indeo ir2_codes le`
  * `libavcodec mpeg1_vlc`
  * `libavcodec mpeg2_vlc`
  * `libavcodec mpeg4 inter_rvlc`
  * `libavcodec mpeg4 intra_rvlc`
  * `libavcodec qcelp_rate_full_codebook`
  * `libavcodec wnv1 code_tab`
  * `libavformat fps_umf2avr AVRational map`
  * `libdjvu MMR bcodes`
  * `libdjvu MMR wcodes`
  * `libfaad2 g_decayslope`
  * `libfaad2 pan_pow_2_30_neg`
  * `libfaad2 pan_pow_2_30_pos`
  * `libfaad2 pan_pow_2_neg`
  * `libfaad2 sa_sqrt_1_minus`
  * `libmng interlace const`
  * `libmpdemux Matroska cook_fl2bps`
  * `libmpdemux tivo Series1AudioWithPTS`
  * `libtheora FrequencyCounts_VP3`
  * `libtheora old FrequencyCounts_VP3`
  * `lpc decode detau table`
  * `lpc encode rmst table`
  * `mp3lib huffman tab1`
  * `mp3lib huffman tab10`
  * `mp3lib huffman tab11`
  * `mp3lib huffman tab12`
  * `mp3lib huffman tab2`
  * `mp3lib huffman tab3`
  * `mp3lib huffman tab5`
  * `mp3lib huffman tab6`
  * `mp3lib huffman tab7`
  * `mp3lib huffman tab8`
  * `mp3lib huffman tab9`
  * `mp3lib huffman tab_c0`
  * `mp3lib huffman tab_c1`
  * `phi init_freq`
  * `redoc3 prime -> "109, 113, 127, 131, 137, 139, 149"`
  * `sfb_16_120 -> "MPEG-2 NBC Fraunhofer sfb_16_120"`
  * `sfb_24_120 -> "MPEG-2 NBC Fraunhofer sfb_24_120"`
  * `sfb_32_120 -> "MPEG-2 NBC Fraunhofer sfb_32_120"`
  * `sfb_48_120 -> "MPEG-2 NBC Fraunhofer sfb_48_120"`
  * `sfb_8_120  -> "MPEG-2 AAC Fraunhofer sfb_8_120" // aac not nbc`
  * `tns_max_bands_tbl_low_delay -> "TNS filter tns_max_bands_tbl_low_delay"`
  * `unlzx table_two ->  "Rar / unlzx table_two"`

## duplicates - removed/changed (name) ##
  * `blowfish_s_init             -> actually one of them was renamed to "CAVE CaveTable"`
  * `Dolby window dol_short_ssr  -> two different sigs, renamed`
  * `FFT and FHT routines rv_tbl -> 8 / 16 versions - merged`
  * `MacGuffin sbits             -> two different sigs, renamed`
  * `Whirlpool rc                -> duplicate removed`

## needs more checking/verification ##
  * `Baseking RCE`
  * `Baseking RCD`
  * `Borland Jfif CrR Table`
  * `Borland Jfif CbB Table`

  * `Nush 64	/ Nessie C_64`
  * `Nush 64	/ Nessie S_64`
  * `HAVAL_wi2`
  * `HAVAL_wi3`
  * `HAVAL_wi4`
  * `HAVAL_wi5`

  * `celptb1`
  * `celptb2`
  * `Thandor game audio codec (? needs verification)`

  * `Boucher randgen1 - sig a bit useless, consts never actually used`
  * `lzari - crappy`

  * `G726 16kbit/s 2bits per sample table - need to do it otherwise`
  * `G726 24kbit/s 3bits per sample table - need to do it otherwise`
  * `G726 32kbit/s 4bits per sample table - need to do it otherwise`

## strange "`_DS`" sigs ##
// many of that "`_DS`" signatures are bit... strange, currently they are removed
  * `ECC_DS`
  * `DESC1_DS`
  * `RIJNDAEL_DS`
  * `RIJNDAEL2_DS`
  * `GOST_DS`
  * `TWOFISH_DS`
  * `TWOFISH1_DS`
  * `ICE1_DS`
  * `MISTY_DS`
  * `SAFER_DS`
  * `SAFER1_DS`
  * `GOST2_DS`
  * `GOST3_DS`
  * `SKIPJACK_DS`
  * `E2_DS`
  * `BIGCREATE_DS`
  * `BIGDESTROY_DS`
  * `FROG`
  * `BIGLIB`
  * `BIGLIB1`
  * `CRC16_DS`